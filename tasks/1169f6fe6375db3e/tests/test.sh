#!/bin/bash
set -u

mkdir -p /logs/verifier
reward=0

fail() {
  echo "$1" >&2
  echo "$reward" > /logs/verifier/reward.txt
  exit 0
}

pkg=/home/user/work/route-lens
out=/home/user/handoff
tarball="$out/acme-route-lens-2.1.0.tgz"
manifest="$out/pack-manifest.json"

[ -d "$pkg" ] || fail "FAIL: package source directory is missing"
[ -d "$out" ] || fail "FAIL: /home/user/handoff is missing"

expected_entries="$(mktemp)"
actual_entries="$(mktemp)"
printf '%s\n' \
  "$tarball" \
  "$manifest" \
  | sort > "$expected_entries"
find "$out" -mindepth 1 -maxdepth 1 -type f | sort > "$actual_entries"
cmp -s "$expected_entries" "$actual_entries" || fail "FAIL: handoff directory must contain exactly the tarball and pack-manifest.json"

expected_pkg="$(mktemp)"
cat > "$expected_pkg" <<'JSON'
{"name":"@acme/route-lens","version":"2.1.0","description":"CLI for normalizing and listing route paths before edge-router deploys.","license":"MIT","type":"commonjs","main":"lib/index.js","bin":{"route-lens":"bin/route-lens.js"},"files":["bin/","lib/","README.md","LICENSE"],"scripts":{"test":"node test/smoke.js"}}
JSON
cmp -s "$expected_pkg" "$pkg/package.json" || fail "FAIL: package.json is not the required minified release metadata"

for rel in bin/route-lens.js lib/index.js lib/normalize.js README.md LICENSE test/smoke.js docs/internal/release-notes.md tmp/debug.log; do
  [ -f "$pkg/$rel" ] || fail "FAIL: source file missing: $rel"
done

grep -qx '97214d3f8ce6f01dff3fe77f87d4f1a438f32e6ee56cb7a9bb255f9b1f5313ef  /home/user/work/route-lens/bin/route-lens.js' <(sha256sum "$pkg/bin/route-lens.js") || fail "FAIL: bin/route-lens.js content changed"
grep -qx '8b3bcfdc4e3cc58d77146c57da5caea5b51e88e1260567732e4c4fb9f4994a4b  /home/user/work/route-lens/lib/index.js' <(sha256sum "$pkg/lib/index.js") || fail "FAIL: lib/index.js content changed"
grep -qx '76917dbfdde73021f84420073ef010443f27bf3c96fed65e188febbb54ab03cf  /home/user/work/route-lens/lib/normalize.js' <(sha256sum "$pkg/lib/normalize.js") || fail "FAIL: lib/normalize.js content changed"
grep -qx '99797db0de1921db09ed241f81815c3f59e6e9fe75087ba92c93351288327386  /home/user/work/route-lens/README.md' <(sha256sum "$pkg/README.md") || fail "FAIL: README.md content changed"
grep -qx 'adc37366f403835c1470ab2df93d3837d4719372fc1ef8593d922e06f033f8b2  /home/user/work/route-lens/LICENSE' <(sha256sum "$pkg/LICENSE") || fail "FAIL: LICENSE content changed"
grep -qx 'e6d3b18218e15d29cd8da1c343727bbcba7367fc2d54b144ceb89d5c1f95419c  /home/user/work/route-lens/test/smoke.js' <(sha256sum "$pkg/test/smoke.js") || fail "FAIL: test/smoke.js content changed"
grep -qx 'e1a2bc9147160b451df169a36b0329a48a535d162156188f59bd55326dfe86a0  /home/user/work/route-lens/docs/internal/release-notes.md' <(sha256sum "$pkg/docs/internal/release-notes.md") || fail "FAIL: internal docs content changed"
grep -qx 'e53d56bb0ab17913fc2b1205a526e0e1295ac1ab88b3ac1f4785c66f9de192ea  /home/user/work/route-lens/tmp/debug.log' <(sha256sum "$pkg/tmp/debug.log") || fail "FAIL: tmp/debug.log content changed"

mode="$(stat -c '%a' "$pkg/bin/route-lens.js")"
[ "$mode" = "755" ] || fail "FAIL: bin/route-lens.js mode is $mode, expected 755"

expected_dir="$(mktemp -d)"
pack_stdout="$(cd "$pkg" && npm pack --json --pack-destination "$expected_dir" 2>/tmp/npm-pack-verify.err)" || fail "FAIL: npm pack failed on repaired source"
[ -f "$expected_dir/acme-route-lens-2.1.0.tgz" ] || fail "FAIL: npm pack did not produce the expected filename"
cmp -s "$expected_dir/acme-route-lens-2.1.0.tgz" "$tarball" || fail "FAIL: handoff tarball does not match npm pack output"

expected_manifest="$(mktemp)"
node -e '
const fs = require("fs");
const item = JSON.parse(process.argv[1])[0];
const manifest = { source: "/home/user/work/route-lens" };
for (const key of Object.keys(item)) manifest[key] = item[key];
fs.writeFileSync(process.argv[2], JSON.stringify(manifest));
' "$pack_stdout" "$expected_manifest" || fail "FAIL: could not build expected manifest"
cmp -s "$expected_manifest" "$manifest" || fail "FAIL: pack-manifest.json content, key order, minification, digest, or trailing newline is incorrect"

node -e '
const fs = require("fs");
const zlib = require("zlib");
const data = zlib.gunzipSync(fs.readFileSync(process.argv[1]));
const text = data.toString("latin1");
for (const forbidden of ["package/test/smoke.js", "package/docs/internal/release-notes.md", "package/tmp/debug.log"]) {
  if (text.includes(forbidden)) process.exit(1);
}
' "$tarball" || fail "FAIL: tarball includes files excluded by package metadata"

reward=1
echo "$reward" > /logs/verifier/reward.txt
echo "ok"
