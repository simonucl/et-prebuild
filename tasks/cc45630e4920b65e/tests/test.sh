#!/bin/bash
set -euo pipefail

mkdir -p /logs/verifier
reward=0

fail() {
  echo "FAIL: $*" >&2
  echo "$reward" > /logs/verifier/reward.txt
  exit 0
}

lab=/home/user/rsync-lab
handoff="$lab/handoff"
baseline="$lab/baseline/site"
desired="$lab/desired/site"
receiver="$lab/receiver/site"

[ -d "$handoff" ] || fail "handoff directory is missing"

expected_files=$'apply-site-update.sh\nitemized-changes.txt\nmanifest.json\nsite-update.batch'
actual_files=$(find "$handoff" -mindepth 1 -maxdepth 1 -type f -printf '%f\n' | sort)
[ "$actual_files" = "$expected_files" ] || fail "handoff does not contain exactly the required files"

[ -x "$handoff/apply-site-update.sh" ] || fail "apply-site-update.sh is not executable"
[ "$(stat -c '%a' "$handoff/site-update.batch")" = "600" ] || fail "site-update.batch must have mode 0600"
[ "$(stat -c '%a' "$handoff/itemized-changes.txt")" = "644" ] || fail "itemized-changes.txt must have mode 0644"
[ "$(stat -c '%a' "$handoff/manifest.json")" = "644" ] || fail "manifest.json must have mode 0644"

grep -q -- '--read-batch=' "$handoff/apply-site-update.sh" || fail "apply script does not use rsync read-batch mode"
! grep -q '/home/user/rsync-lab' "$handoff/apply-site-update.sh" || fail "apply script is not relocatable"

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

mkdir -p "$tmp/expected-receiver" "$tmp/expected-handoff" "$tmp/apply/site"
rsync -a --delete "$baseline/" "$tmp/expected-receiver/site/"
rsync -a --delete --checksum --itemize-changes \
  --write-batch="$tmp/expected-handoff/site-update.batch" \
  "$desired/" "$tmp/expected-receiver/site/" \
  > "$tmp/expected-handoff/itemized-changes.txt"

cmp -s "$tmp/expected-handoff/itemized-changes.txt" "$handoff/itemized-changes.txt" \
  || fail "itemized-changes.txt does not match rsync batch generation output"

rsync -a --delete "$baseline/" "$tmp/apply/site/"
mkdir -p "$tmp/portable"
cp "$handoff/site-update.batch" "$handoff/apply-site-update.sh" "$tmp/portable/"
bash "$tmp/portable/apply-site-update.sh" "$tmp/apply/site/" > "$tmp/apply.stdout"

python3 - <<'PY' "$desired" "$tmp/apply/site" || fail "applied batch does not reproduce desired tree"
import filecmp
import os
import stat
import sys
from pathlib import Path

left = Path(sys.argv[1])
right = Path(sys.argv[2])

def entries(root):
    out = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        st = path.lstat()
        if stat.S_ISLNK(st.st_mode):
            out[rel] = ("symlink", os.readlink(path), stat.S_IMODE(st.st_mode))
        elif stat.S_ISDIR(st.st_mode):
            out[rel] = ("dir", None, stat.S_IMODE(st.st_mode))
        elif stat.S_ISREG(st.st_mode):
            out[rel] = ("file", path.read_bytes(), stat.S_IMODE(st.st_mode))
        else:
            out[rel] = ("other", None, stat.S_IMODE(st.st_mode))
    return out

if entries(left) != entries(right):
    sys.exit(1)
PY

python3 - <<'PY' "$desired" "$receiver" || fail "receiver tree does not match desired tree"
import os
import stat
import sys
from pathlib import Path

def snapshot(root):
    root = Path(root)
    out = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        st = path.lstat()
        if stat.S_ISLNK(st.st_mode):
            out[rel] = ("symlink", os.readlink(path), stat.S_IMODE(st.st_mode))
        elif stat.S_ISDIR(st.st_mode):
            out[rel] = ("dir", None, stat.S_IMODE(st.st_mode))
        elif stat.S_ISREG(st.st_mode):
            out[rel] = ("file", path.read_bytes(), stat.S_IMODE(st.st_mode))
        else:
            out[rel] = ("other", None, stat.S_IMODE(st.st_mode))
    return out

if snapshot(sys.argv[1]) != snapshot(sys.argv[2]):
    sys.exit(1)
PY

python3 - <<'PY' "$handoff" || fail "manifest content, key order, minification, or hash is incorrect"
import hashlib
import json
import sys
from pathlib import Path

handoff = Path(sys.argv[1])
manifest_path = handoff / "manifest.json"
raw = manifest_path.read_bytes()
if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
    sys.exit(1)
line = raw[:-1]
if b"\n" in line:
    sys.exit(1)
expected = {
    "batch": "site-update.batch",
    "apply_script": "apply-site-update.sh",
    "source_root": "site/",
    "options": ["-a", "--delete", "--checksum", "--itemize-changes"],
    "changes": (handoff / "itemized-changes.txt").read_text().splitlines(),
    "batch_sha256": hashlib.sha256((handoff / "site-update.batch").read_bytes()).hexdigest(),
}
expected_raw = json.dumps(expected, separators=(",", ":")).encode() + b"\n"
if raw != expected_raw:
    sys.exit(1)
PY

reward=1
echo "$reward" > /logs/verifier/reward.txt
