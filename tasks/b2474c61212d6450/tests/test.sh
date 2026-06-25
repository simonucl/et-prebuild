#!/bin/bash
set -u

mkdir -p /logs/verifier

fail() {
  echo "$1"
  echo 0 > /logs/verifier/reward.txt
  exit 0
}

pkg_dir=/home/user/npm-lab/stream-redactor
dist_dir=/home/user/npm-lab/dist
tarball="$dist_dir/acme-stream-redactor-1.2.3.tgz"
manifest="$dist_dir/pack-manifest.json"

[ -d "$pkg_dir" ] || fail "missing package source directory"
[ -d "$dist_dir" ] || fail "missing dist directory"
[ -f "$tarball" ] || fail "missing final npm tarball"
[ -f "$manifest" ] || fail "missing pack-manifest.json"

node <<'NODE' || fail "package.json metadata is not repaired"
const fs = require("fs");
const pkg = JSON.parse(fs.readFileSync("/home/user/npm-lab/stream-redactor/package.json", "utf8"));
const expectedFiles = ["index.js", "cli.js", "rules/default.json", "README.md", "LICENSE"];
if (pkg.name !== "@acme/stream-redactor") process.exit(1);
if (pkg.version !== "1.2.3") process.exit(1);
if (pkg.main !== "index.js") process.exit(1);
if (!pkg.bin || pkg.bin["stream-redactor"] !== "cli.js" || Object.keys(pkg.bin).length !== 1) process.exit(1);
if (JSON.stringify(pkg.files) !== JSON.stringify(expectedFiles)) process.exit(1);
NODE

actual_files=$(find "$dist_dir" -maxdepth 1 -type f -printf '%f\n' | sort)
expected_files=$'acme-stream-redactor-1.2.3.tgz\npack-manifest.json'
[ "$actual_files" = "$expected_files" ] || fail "dist directory must contain exactly the tarball and manifest"

tmp=$(mktemp -d)
mkdir -p "$tmp/pack" "$tmp/install"
pack_json="$tmp/npm-pack.json"
npm pack --json --pack-destination "$tmp/pack" "$pkg_dir" > "$pack_json" 2>"$tmp/npm-pack.err" || {
  cat "$tmp/npm-pack.err"
  fail "npm pack failed on the repaired source tree"
}

cmp -s "$tmp/pack/acme-stream-redactor-1.2.3.tgz" "$tarball" || fail "tarball does not match npm pack output for the repaired package"

expected_manifest="$tmp/expected-manifest.json"
node - "$pack_json" "$expected_manifest" <<'NODE' || fail "could not build expected manifest"
const fs = require("fs");
const packPath = process.argv[2];
const outPath = process.argv[3];
const pack = JSON.parse(fs.readFileSync(packPath, "utf8"))[0];
const manifest = {
  name: pack.name,
  version: pack.version,
  filename: pack.filename,
  shasum: pack.shasum,
  integrity: pack.integrity,
  files: pack.files.map(file => file.path)
};
fs.writeFileSync(outPath, JSON.stringify(manifest) + "\n");
NODE

cmp -s "$expected_manifest" "$manifest" || fail "pack-manifest.json does not match npm pack --json metadata"

tar -tzf "$tarball" | sort > "$tmp/tar-list" || fail "tarball is not a readable gzip tar archive"
cat > "$tmp/expected-list" <<'EOF'
package/LICENSE
package/README.md
package/cli.js
package/index.js
package/package.json
package/rules/default.json
EOF
cmp -s "$tmp/expected-list" "$tmp/tar-list" || fail "tarball contains the wrong package members"

npm install --offline --ignore-scripts --no-audit --no-fund --prefix "$tmp/install" "$tarball" >/dev/null 2>"$tmp/npm-install.err" || {
  cat "$tmp/npm-install.err"
  fail "packed tarball cannot be installed locally"
}

printf 'api_key=abc123 token=local password=secret\n' | "$tmp/install/node_modules/.bin/stream-redactor" > "$tmp/cli-output" || fail "installed CLI did not run"
expected_cli='api_key=[REDACTED] token=[REDACTED] password=[REDACTED]'
actual_cli=$(tr -d '\n' < "$tmp/cli-output")
[ "$actual_cli" = "$expected_cli" ] || fail "installed CLI output is incorrect"

echo 1 > /logs/verifier/reward.txt
exit 0
