#!/bin/bash
set -u

mkdir -p /logs/verifier
reward=0

fail() {
  echo "FAIL: $1"
  echo "$reward" > /logs/verifier/reward.txt
  exit 0
}

src=/home/user/release/source
receiver=/home/user/release/receiver.git
out=/home/user/release/handoff
bundle=$out/edge-collector-v1.9.0.bundle
patch_dir=$out/patches
manifest=$out/manifest.json
archive=$out/edge-collector-v1.9.0-handoff.tar.gz
name=edge-collector-v1.9.0-handoff
epoch=1711929600

[ -f "$bundle" ] || fail "missing bundle"
[ -d "$patch_dir" ] || fail "missing patches directory"
[ -f "$manifest" ] || fail "missing manifest"
[ -f "$archive" ] || fail "missing archive"

base_commit=$(git -C "$src" rev-parse v1.8.0) || fail "cannot read base commit"
target_commit=$(git -C "$src" rev-parse release/v1.9) || fail "cannot read target commit"

heads=$(git bundle list-heads "$bundle" 2>/dev/null | LC_ALL=C sort) || fail "bundle is not readable"
expected_heads=$(printf '%s refs/heads/release/v1.9\n%s refs/tags/v1.9.0\n' "$target_commit" "$target_commit" | LC_ALL=C sort)
[ "$heads" = "$expected_heads" ] || fail "bundle heads are not exactly release/v1.9 and v1.9.0"

python3 - "$bundle" "$base_commit" <<'PY' || fail "bundle does not record v1.8.0 as prerequisite"
from pathlib import Path
import sys

bundle = Path(sys.argv[1])
base = sys.argv[2].encode()
header = bundle.read_bytes().split(b"\n\n", 1)[0].splitlines()
want = b"-" + base
if not any(line == want or line.startswith(want + b" ") for line in header):
    raise SystemExit(1)
PY
git -C "$receiver" bundle verify "$bundle" >/tmp/bundle.verify 2>&1 || fail "bundle does not verify against receiver.git"

tmpclone=$(mktemp -d)
tmpexpected=$(mktemp -d)
tmpextract=$(mktemp -d)
trap 'rm -rf "$tmpclone" "$tmpexpected" "$tmpextract"' EXIT

git clone -q "$receiver" "$tmpclone/repo" || fail "cannot clone receiver"
git -C "$tmpclone/repo" fetch -q "$bundle" \
  refs/heads/release/v1.9:refs/heads/release/v1.9 \
  refs/tags/v1.9.0:refs/tags/v1.9.0 || fail "cannot fetch bundle refs into receiver clone"
[ "$(git -C "$tmpclone/repo" rev-parse refs/heads/release/v1.9)" = "$target_commit" ] || fail "fetched release branch points at wrong commit"
[ "$(git -C "$tmpclone/repo" rev-parse refs/tags/v1.9.0)" = "$target_commit" ] || fail "fetched tag points at wrong commit"

git -C "$src" format-patch --binary --full-index --output-directory "$tmpexpected/patches" v1.8.0..release/v1.9 >/dev/null \
  || fail "cannot regenerate expected patches"
expected_patch_list=$(cd "$tmpexpected/patches" && find . -maxdepth 1 -type f -name '*.patch' -printf '%P\n' | LC_ALL=C sort)
actual_patch_list=$(cd "$patch_dir" && find . -maxdepth 1 -type f -name '*.patch' -printf '%P\n' | LC_ALL=C sort)
[ "$actual_patch_list" = "$expected_patch_list" ] || fail "patch filenames do not match git format-patch output"
while IFS= read -r patch; do
  [ -n "$patch" ] || continue
  cmp -s "$tmpexpected/patches/$patch" "$patch_dir/$patch" || fail "$patch does not match git format-patch --binary --full-index output"
done <<EOF
$expected_patch_list
EOF

python3 - "$src" "$out" "$manifest" "$archive" "$name" "$epoch" <<'PY' || fail "manifest or archive validation failed"
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile

src = Path(sys.argv[1])
out = Path(sys.argv[2])
manifest_path = Path(sys.argv[3])
archive_path = Path(sys.argv[4])
top = sys.argv[5]
epoch = int(sys.argv[6])

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git_rev(rev: str) -> str:
    return subprocess.check_output(["git", "-C", str(src), "rev-parse", rev], text=True).strip()

raw = manifest_path.read_bytes()
if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
    raise SystemExit("manifest newline is wrong")
if b" " in raw or b"\t" in raw:
    raise SystemExit("manifest is not minified")

actual = json.loads(raw)
patches = []
for patch in sorted((out / "patches").glob("*.patch")):
    patches.append({"path": f"patches/{patch.name}", "sha256": sha256(patch)})

expected = {
    "schema_version": 1,
    "project": "edge-collector",
    "base_tag": "v1.8.0",
    "base_commit": git_rev("v1.8.0"),
    "target_ref": "refs/heads/release/v1.9",
    "target_tag": "v1.9.0",
    "target_commit": git_rev("release/v1.9"),
    "bundle": {
        "path": "edge-collector-v1.9.0.bundle",
        "sha256": sha256(out / "edge-collector-v1.9.0.bundle"),
    },
    "patches": patches,
    "archive": {
        "path": "edge-collector-v1.9.0-handoff.tar.gz",
        "file_count": 2 + len(patches),
    },
}
expected_raw = (json.dumps(expected, separators=(",", ":")) + "\n").encode()
if raw != expected_raw:
    raise SystemExit("manifest content, key order, minification, or hashes are incorrect")

with archive_path.open("rb") as f:
    header = f.read(10)
if len(header) != 10 or header[:2] != b"\x1f\x8b":
    raise SystemExit("archive is not gzip")
if header[3] & 0x08:
    raise SystemExit("gzip header stores an original filename")
if header[4:8] != b"\x00\x00\x00\x00":
    raise SystemExit("gzip header stores a timestamp")

expected_names = [
    f"{top}",
    f"{top}/edge-collector-v1.9.0.bundle",
    f"{top}/manifest.json",
    f"{top}/patches",
]
expected_names.extend(f"{top}/patches/{Path(p['path']).name}" for p in patches)

with tarfile.open(archive_path, "r:gz") as tf:
    members = tf.getmembers()
    names = [m.name for m in members]
    if names != expected_names:
        raise SystemExit(f"archive member order or names are wrong: {names!r}")
    for m in members:
        if m.uid != 0 or m.gid != 0:
            raise SystemExit(f"{m.name} does not use numeric 0/0 ownership")
        if m.mtime != epoch:
            raise SystemExit(f"{m.name} has wrong mtime")
        if m.isdir():
            if (m.mode & 0o777) != 0o755:
                raise SystemExit(f"{m.name} directory mode is wrong")
        elif m.isfile():
            if (m.mode & 0o777) != 0o644:
                raise SystemExit(f"{m.name} file mode is wrong")
        else:
            raise SystemExit(f"{m.name} is not a regular file or directory")
    extracted = {}
    for m in members:
        if m.isfile():
            data = tf.extractfile(m).read()
            extracted[m.name] = hashlib.sha256(data).hexdigest()

if extracted[f"{top}/edge-collector-v1.9.0.bundle"] != sha256(out / "edge-collector-v1.9.0.bundle"):
    raise SystemExit("archive bundle content differs from handoff bundle")
if extracted[f"{top}/manifest.json"] != sha256(out / "manifest.json"):
    raise SystemExit("archive manifest content differs from handoff manifest")
for patch in patches:
    filename = Path(patch["path"]).name
    if extracted[f"{top}/patches/{filename}"] != sha256(out / "patches" / filename):
        raise SystemExit(f"archive patch {filename} differs from handoff patch")
PY

reward=1
echo "$reward" > /logs/verifier/reward.txt
exit 0
