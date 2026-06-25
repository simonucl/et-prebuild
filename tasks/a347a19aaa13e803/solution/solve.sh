#!/bin/bash
set -euo pipefail

root=${ROOT_PREFIX:-}
pkg="$root/home/user/npm-lab/src/acme-logship"
dist="$root/home/user/npm-lab/dist"

cat > "$pkg/package.json" <<'EOF'
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

cat > "$pkg/lib/index.js" <<'EOF'
function formatLine(level, message) {
  return JSON.stringify({ level, message });
}

module.exports = { formatLine };
EOF

chmod 0755 "$pkg/bin/logship.js"
mkdir -p "$dist"
rm -f "$dist/acme-logship-0.6.0.tgz" "$dist/packument.json"
npm pack --json --pack-destination "$dist" "$pkg" > "$dist/packument.json"
