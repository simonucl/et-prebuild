#!/bin/bash
set -u

mkdir -p /logs/verifier
reward=0

handoff=/home/user/npm-lab/handoff
pkg=/home/user/npm-lab/widget-kit
tarball="$handoff/acme-widget-kit-1.6.4.tgz"
manifest="$handoff/package-manifest.json"
sums="$handoff/SHA256SUMS"

fail() {
  echo "FAIL: $*" >&2
  echo "$reward" > /logs/verifier/reward.txt
  exit 0
}

[ -d "$handoff" ] || fail "handoff directory is missing"
mapfile -t handoff_files < <(find "$handoff" -maxdepth 1 -type f -printf '%f\n' | sort)
expected_handoff=$'SHA256SUMS\nacme-widget-kit-1.6.4.tgz\npackage-manifest.json'
actual_handoff=$(printf '%s\n' "${handoff_files[@]}")
[ "$actual_handoff" = "$expected_handoff" ] || fail "handoff directory must contain exactly the required files"

[ -f "$tarball" ] || fail "package tarball is missing"
[ -f "$manifest" ] || fail "package-manifest.json is missing"
[ -f "$sums" ] || fail "SHA256SUMS is missing"

expected_sum="$(sha256sum "$tarball" | awk '{print $1}')  acme-widget-kit-1.6.4.tgz"
actual_sum="$(cat "$sums")"
[ "$actual_sum" = "$expected_sum" ] || fail "SHA256SUMS does not match the tarball"
[ "$(tail -c 1 "$sums" | od -An -t x1 | tr -d ' ')" = "0a" ] || fail "SHA256SUMS must end with a newline"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

tar -xzf "$tarball" -C "$tmp" || fail "tarball is not a valid gzip tar archive"
tar -tf "$tarball" > "$tmp/listing.txt" || fail "could not list tarball"
cat > "$tmp/expected-listing.txt" <<'EOF'
package/LICENSE
package/dist/cli.cjs
package/dist/index.cjs
package/package.json
package/README.md
package/dist/index.mjs
package/dist/index.d.ts
EOF
diff -u "$tmp/expected-listing.txt" "$tmp/listing.txt" || fail "tarball members or archive order are wrong"

[ ! -e "$tmp/package/src" ] || fail "tarball must not contain src/"
[ ! -e "$tmp/package/scripts" ] || fail "tarball must not contain scripts/"
cmp -s "$pkg/LICENSE" "$tmp/package/LICENSE" || fail "LICENSE content differs"
cmp -s "$pkg/README.md" "$tmp/package/README.md" || fail "README.md content differs"

node - <<'NODE' "$tmp/package"
const path = require('node:path');
const pkgDir = process.argv[2];
const mod = require(path.join(pkgDir, 'dist/index.cjs'));
if (mod.renderWidget('  HELLO  ') !== 'widget:hello') {
  process.exit(41);
}
NODE
[ $? -eq 0 ] || fail "generated CommonJS module does not behave correctly"

head -n 1 "$tmp/package/dist/cli.cjs" | grep -qx '#!/usr/bin/env node' || fail "CLI file is missing node shebang"
mode_cli=$(tar -tvf "$tarball" package/dist/cli.cjs | awk '{print $1}')
[ "$mode_cli" = "-rwxr-xr-x" ] || fail "CLI tar mode must be executable"
for p in package/LICENSE package/dist/index.cjs package/package.json package/README.md package/dist/index.mjs package/dist/index.d.ts; do
  mode=$(tar -tvf "$tarball" "$p" | awk '{print $1}')
  [ "$mode" = "-rw-r--r--" ] || fail "$p tar mode must be 0644"
done

python3 - <<'PY' "$tarball" "$manifest"
import base64
import hashlib
import json
import sys
import tarfile
from pathlib import Path

tarball = Path(sys.argv[1])
manifest = Path(sys.argv[2])
text = manifest.read_text(encoding="utf-8")
if not text.endswith("\n") or text.endswith("\n\n"):
    raise SystemExit("manifest newline is wrong")
if "\n" in text[:-1]:
    raise SystemExit("manifest must be minified on one line")
data = json.loads(text)
if list(data.keys()) != ["package", "version", "tarball", "sha256", "sha1", "integrity", "entry_count", "files"]:
    raise SystemExit("manifest top-level key order is wrong")
blob = tarball.read_bytes()
expected_top = {
    "package": "@acme/widget-kit",
    "version": "1.6.4",
    "tarball": "acme-widget-kit-1.6.4.tgz",
    "sha256": hashlib.sha256(blob).hexdigest(),
    "sha1": hashlib.sha1(blob).hexdigest(),
    "integrity": "sha512-" + base64.b64encode(hashlib.sha512(blob).digest()).decode("ascii"),
}
for key, value in expected_top.items():
    if data.get(key) != value:
        raise SystemExit(f"manifest {key} is wrong")

files = []
with tarfile.open(tarball, "r:gz") as tf:
    for member in tf.getmembers():
        extracted = tf.extractfile(member)
        content = extracted.read() if extracted is not None else b""
        files.append({
            "path": member.name,
            "mode": format(member.mode & 0o7777, "04o"),
            "size": member.size,
            "sha256": hashlib.sha256(content).hexdigest(),
        })
if data.get("entry_count") != len(files):
    raise SystemExit("manifest entry_count is wrong")
if data.get("files") != files:
    raise SystemExit("manifest files do not match tar members")
for item in data.get("files", []):
    if list(item.keys()) != ["path", "mode", "size", "sha256"]:
        raise SystemExit("manifest file entry key order is wrong")
PY
[ $? -eq 0 ] || fail "package-manifest.json is incorrect"

reward=1
echo "$reward" > /logs/verifier/reward.txt
exit 0
