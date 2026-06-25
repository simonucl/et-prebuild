#!/bin/bash
set -euo pipefail

pkg=/home/user/work/route-lens
out=/home/user/handoff

cat > "$pkg/package.json" <<'JSON'
{"name":"@acme/route-lens","version":"2.1.0","description":"CLI for normalizing and listing route paths before edge-router deploys.","license":"MIT","type":"commonjs","main":"lib/index.js","bin":{"route-lens":"bin/route-lens.js"},"files":["bin/","lib/","README.md","LICENSE"],"scripts":{"test":"node test/smoke.js"}}
JSON

chmod 0755 "$pkg/bin/route-lens.js"
rm -rf "$out"
mkdir -p "$out"

pack_json="$(cd "$pkg" && npm pack --json --pack-destination "$out")"
node -e '
const fs = require("fs");
const item = JSON.parse(process.argv[1])[0];
const manifest = { source: "/home/user/work/route-lens" };
for (const key of Object.keys(item)) manifest[key] = item[key];
fs.writeFileSync("/home/user/handoff/pack-manifest.json", JSON.stringify(manifest));
' "$pack_json"
