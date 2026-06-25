#!/bin/bash
set -u

reward=0
root=${ROOT_PREFIX:-}
log_dir=${VERIFIER_LOG_DIR:-/logs/verifier}
mkdir -p "$log_dir"

fail() {
  echo "FAIL: $1" >&2
  echo "$reward" > "$log_dir/reward.txt"
  exit 0
}

pkg="$root/home/user/npm-lab/src/acme-logship"
dist="$root/home/user/npm-lab/dist"
tarball="$dist/acme-logship-0.6.0.tgz"
packument="$dist/packument.json"

[ -d "$pkg" ] || fail "missing source package directory"
[ -f "$pkg/package.json" ] || fail "missing package.json"
[ -x "$pkg/bin/logship.js" ] || fail "bin/logship.js is not executable"
[ -f "$tarball" ] || fail "missing npm package tarball"
[ -f "$packument" ] || fail "missing packument.json"

expected_manifest=$(mktemp)
cat > "$expected_manifest" <<'EOF'
{
  "name": "@acme/logship",
  "version": "0.6.0",
  "description": "Offline log shipping CLI",
  "license": "MIT",
  "bin": {
    "logship": "bin/logship.js"
  },
  "files": [
    "bin/",
    "lib/",
    "README.md",
    "LICENSE"
  ]
}
EOF

cmp -s "$expected_manifest" "$pkg/package.json" || fail "package.json content, key order, or trailing newline is incorrect"

cli_output=$(node "$pkg/bin/logship.js" warn "disk low" 2>/tmp/logship.err) || fail "logship CLI execution failed"
[ "$cli_output" = '{"level":"warn","message":"disk low"}' ] || fail "logship CLI output is incorrect"

tmpdir=$(mktemp -d)
expected_pack_json="$tmpdir/expected-pack.json"
expected_dist="$tmpdir/dist"
mkdir -p "$expected_dist"

npm pack --json --pack-destination "$expected_dist" "$pkg" > "$expected_pack_json" 2>"$tmpdir/npm.err" || fail "npm pack could not regenerate expected artifact"
expected_tarball="$expected_dist/acme-logship-0.6.0.tgz"
[ -f "$expected_tarball" ] || fail "regenerated npm tarball has the wrong filename"

cmp -s "$expected_tarball" "$tarball" || fail "submitted tarball does not match npm pack output for the repaired source"

python3 - "$expected_pack_json" "$packument" "$tarball" <<'PY'
import hashlib
import json
import sys
import tarfile
from pathlib import Path

expected_path, actual_path, tarball_path = map(Path, sys.argv[1:])

try:
    expected = json.loads(expected_path.read_text())
    actual = json.loads(actual_path.read_text())
except Exception as exc:
    raise SystemExit(f"packument is not valid JSON: {exc}")

if actual != expected:
    raise SystemExit("packument.json does not match npm pack --json output")

if not isinstance(actual, list) or len(actual) != 1:
    raise SystemExit("packument must be a single-element npm pack JSON array")

entry = actual[0]
required = {
    "id": "@acme/logship@0.6.0",
    "name": "@acme/logship",
    "version": "0.6.0",
    "filename": "acme-logship-0.6.0.tgz",
    "entryCount": 5,
}
for key, value in required.items():
    if entry.get(key) != value:
        raise SystemExit(f"packument field {key!r} is incorrect")

files = entry.get("files")
expected_files = [
    {"path": "LICENSE", "size": 4, "mode": 420},
    {"path": "README.md", "size": 59, "mode": 420},
    {"path": "bin/logship.js", "size": 193, "mode": 493},
    {"path": "lib/index.js", "size": 119, "mode": 420},
    {"path": "package.json", "size": 238, "mode": 420},
]
if files != expected_files:
    raise SystemExit(f"packed file list, sizes, or modes are incorrect: {files!r}")

with tarfile.open(tarball_path, "r:gz") as tf:
    names = tf.getnames()
    if names != [
        "package/LICENSE",
        "package/lib/index.js",
        "package/bin/logship.js",
        "package/package.json",
        "package/README.md",
    ]:
        raise SystemExit(f"tar member order is incorrect: {names!r}")
    for member in tf.getmembers():
        if member.uid != 0 or member.gid != 0:
            raise SystemExit("tar members must use numeric 0/0 ownership")
    if any("private-release-notes" in name or "/notes/" in name for name in names):
        raise SystemExit("private notes were included in the package")

sha1 = hashlib.sha1(tarball_path.read_bytes()).hexdigest()
if entry.get("shasum") != sha1:
    raise SystemExit("packument shasum does not match the tarball")
PY

if [ $? -ne 0 ]; then
  fail "packument metadata or tarball contents are incorrect"
fi

reward=1
echo "$reward" > "$log_dir/reward.txt"
exit 0
