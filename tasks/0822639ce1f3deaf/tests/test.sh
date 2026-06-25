#!/bin/bash
set -u

mkdir -p /logs/verifier
reward=0
fail() {
  echo "FAIL: $*" >&2
  echo "$reward" > /logs/verifier/reward.txt
  exit 1
}

repo=/home/user/work/telemetry-agent
receiver=/home/user/work/receiver.git
out=/home/user/delivery
bundle=$out/telemetry-agent-1.7.3.bundle
patch_archive=$out/telemetry-agent-1.7.3-patches.tar.gz
manifest=$out/manifest.json
branch=refs/heads/release/1.7.3
tag=refs/tags/v1.7.3
base=v1.7.0

[ -d "$out" ] || fail "delivery directory is missing"
mapfile -t deliverables < <(find "$out" -maxdepth 1 -type f -printf '%f\n' | sort)
expected=$'manifest.json\ntelemetry-agent-1.7.3-patches.tar.gz\ntelemetry-agent-1.7.3.bundle'
actual=$(printf '%s\n' "${deliverables[@]}")
[ "$actual" = "$expected" ] || fail "delivery contains unexpected files: $actual"

[ -s "$bundle" ] || fail "bundle is missing or empty"
[ -s "$patch_archive" ] || fail "patch archive is missing or empty"
[ -s "$manifest" ] || fail "manifest is missing or empty"
[ "$(tail -c 1 "$manifest" | od -An -t x1 | tr -d ' \n')" = "0a" ] || fail "manifest does not end with one newline"
python3 - "$manifest" <<'PY' || fail "manifest is not minified JSON with the required key order"
import json, sys
from pathlib import Path
p = Path(sys.argv[1])
b = p.read_bytes()
if b.count(b"\n") != 1 or not b.endswith(b"\n"):
    raise SystemExit(1)
text = b.decode()
obj = json.loads(text)
if text != json.dumps(obj, separators=(",", ":")) + "\n":
    raise SystemExit(1)
keys = ["bundle","patch_archive","source_branch","release_tag","base_tag","prerequisite_commit","release_commit","included_commits","patches","bundle_sha256","patch_archive_sha256"]
if list(obj.keys()) != keys:
    raise SystemExit(1)
for item in obj["included_commits"]:
    if list(item.keys()) != ["commit", "subject"]:
        raise SystemExit(1)
PY

base_commit=$(git -C "$repo" rev-parse "$base^{commit}") || fail "cannot resolve base commit"
release_commit=$(git -C "$repo" rev-parse "$branch^{commit}") || fail "cannot resolve release branch"
release_tag_oid=$(git -C "$repo" rev-parse "$tag") || fail "cannot resolve release tag"

grep -aEq "^-$base_commit( |$)" "$bundle" || fail "bundle does not record $base as a prerequisite"
mapfile -t heads < <(git -C "$repo" bundle list-heads "$bundle" | sort -k2)
expected_heads=$(printf '%s %s\n%s %s\n' "$release_commit" "$branch" "$release_tag_oid" "$tag" | sort -k2)
actual_heads=$(printf '%s\n' "${heads[@]}")
[ "$actual_heads" = "$expected_heads" ] || fail "bundle advertises wrong refs: $actual_heads"
printf '%s\n' "$actual_heads" | grep -q 'refs/heads/main' && fail "bundle advertises main"
printf '%s\n' "$actual_heads" | grep -q 'HEAD' && fail "bundle advertises HEAD"
printf '%s\n' "$actual_heads" | grep -q 'experiment' && fail "bundle advertises experiment refs"

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
git clone "$receiver" "$tmp/receiver" >/dev/null 2>&1 || fail "cannot clone receiver"
verify_out=$(git -C "$tmp/receiver" bundle verify "$bundle" 2>&1) || fail "receiver cannot verify bundle: $verify_out"
printf '%s\n' "$verify_out" | grep -q "$base_commit" || fail "bundle verify output does not mention prerequisite"
git -C "$tmp/receiver" fetch "$bundle" "$branch:$branch" "$tag:$tag" >/dev/null 2>&1 || fail "receiver cannot fetch branch and tag"
[ "$(git -C "$tmp/receiver" rev-parse "$branch^{commit}")" = "$release_commit" ] || fail "fetched branch points at wrong commit"
[ "$(git -C "$tmp/receiver" rev-parse "$tag^{commit}")" = "$release_commit" ] || fail "fetched tag points at wrong commit"

python3 - "$patch_archive" <<'PY' || fail "gzip header is not deterministic"
import sys
b = open(sys.argv[1], "rb").read(10)
if b[:2] != b"\x1f\x8b":
    raise SystemExit(1)
flags = b[3]
mtime = int.from_bytes(b[4:8], "little")
if flags & 0x08 or mtime != 0:
    raise SystemExit(1)
PY

mapfile -t tar_entries < <(tar -tzf "$patch_archive")
expected_entries=$'patches/\npatches/0001-Bump-release-version-to-1.7.3.patch\npatches/0002-Normalize-event-kinds-for-release.patch\npatches/0003-Tighten-telemetry-defaults.patch'
actual_entries=$(printf '%s\n' "${tar_entries[@]}")
[ "$actual_entries" = "$expected_entries" ] || fail "patch archive entries are incorrect: $actual_entries"
tar -tvzf "$patch_archive" | awk '{print $1, $2, $3, $4, $5, $6}' > "$tmp/tar_listing"
awk '$2 != "0/0" || $4 != "2026-02-10" || $5 != "00:00" {bad=1} END{exit bad}' "$tmp/tar_listing" || fail "patch archive metadata is not normalized"

mkdir -p "$tmp/patches"
tar -xzf "$patch_archive" -C "$tmp/patches" || fail "cannot unpack patch archive"
git clone "$receiver" "$tmp/apply" >/dev/null 2>&1 || fail "cannot clone receiver for patch application"
git -C "$tmp/apply" config user.name "Verifier"
git -C "$tmp/apply" config user.email "verifier@example.invalid"
git -C "$tmp/apply" am "$tmp/patches"/patches/*.patch >/dev/null 2>&1 || fail "patch series does not apply cleanly"
applied_tree=$(git -C "$tmp/apply" rev-parse HEAD^{tree})
release_tree=$(git -C "$repo" rev-parse "$branch^{tree}")
[ "$applied_tree" = "$release_tree" ] || fail "patch series tree does not match release branch"

python3 - "$manifest" "$repo" "$bundle" "$patch_archive" "$base_commit" "$release_commit" <<'PY' || fail "manifest values are incorrect"
import hashlib, json, subprocess, sys
manifest, repo, bundle, patch_archive, base_commit, release_commit = sys.argv[1:]
with open(manifest, "r", encoding="utf-8") as f:
    data = json.load(f)
expected = {
    "bundle": "telemetry-agent-1.7.3.bundle",
    "patch_archive": "telemetry-agent-1.7.3-patches.tar.gz",
    "source_branch": "refs/heads/release/1.7.3",
    "release_tag": "refs/tags/v1.7.3",
    "base_tag": "v1.7.0",
    "prerequisite_commit": base_commit,
    "release_commit": release_commit,
    "patches": [
        "0001-Bump-release-version-to-1.7.3.patch",
        "0002-Normalize-event-kinds-for-release.patch",
        "0003-Tighten-telemetry-defaults.patch",
    ],
}
for k, v in expected.items():
    if data.get(k) != v:
        raise SystemExit(1)
log = subprocess.check_output(["git", "-C", repo, "log", "--reverse", "--format=%H%x00%s", "v1.7.0..refs/heads/release/1.7.3"], text=True)
commits = [{"commit": line.split("\0", 1)[0], "subject": line.split("\0", 1)[1]} for line in log.splitlines()]
if data["included_commits"] != commits:
    raise SystemExit(1)
for key, path in [("bundle_sha256", bundle), ("patch_archive_sha256", patch_archive)]:
    h = hashlib.sha256(open(path, "rb").read()).hexdigest()
    if data.get(key) != h:
        raise SystemExit(1)
PY

reward=1
echo 1 > /logs/verifier/reward.txt
exit 0
