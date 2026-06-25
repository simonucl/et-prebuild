#!/bin/bash
set -euo pipefail

pkg_dir=/home/user/npm-lab/stream-redactor
dist_dir=/home/user/npm-lab/dist

node <<'NODE'
const fs = require("fs");
const path = "/home/user/npm-lab/stream-redactor/package.json";
const pkg = JSON.parse(fs.readFileSync(path, "utf8"));

pkg.name = "@acme/stream-redactor";
pkg.version = "1.2.3";
pkg.main = "index.js";
pkg.bin = { "stream-redactor": "cli.js" };
pkg.files = ["index.js", "cli.js", "rules/default.json", "README.md", "LICENSE"];

fs.writeFileSync(path, JSON.stringify(pkg, null, 2) + "\n");
NODE

rm -rf "$dist_dir"
mkdir -p "$dist_dir"
npm pack --json --pack-destination "$dist_dir" "$pkg_dir" > /tmp/stream-redactor-pack.json

node <<'NODE'
const fs = require("fs");
const pack = JSON.parse(fs.readFileSync("/tmp/stream-redactor-pack.json", "utf8"))[0];
const manifest = {
  name: pack.name,
  version: pack.version,
  filename: pack.filename,
  shasum: pack.shasum,
  integrity: pack.integrity,
  files: pack.files.map(file => file.path)
};
fs.writeFileSync("/home/user/npm-lab/dist/pack-manifest.json", JSON.stringify(manifest) + "\n");
NODE
