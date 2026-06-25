#!/bin/bash
set -euo pipefail

src=/app/module-src
dst=/app/goproxy/example.internal/edge/ratelimit/@v
version=v0.9.0
module=example.internal/edge/ratelimit

rm -f "$dst"/*
printf '%s\n' "$version" > "$dst/list"
printf '{"Version":"%s","Time":"2026-06-01T10:30:00Z"}\n' "$version" > "$dst/$version.info"
cp "$src/go.mod" "$dst/$version.mod"

python3 - <<'PY'
import hashlib
import json
import os
import stat
import zipfile
from collections import OrderedDict
from pathlib import Path

src = Path("/app/module-src")
dst = Path("/app/goproxy/example.internal/edge/ratelimit/@v")
module = "example.internal/edge/ratelimit"
version = "v0.9.0"
members = ["go.mod", "limiter.go", "limiter_test.go", "README.md"]
zip_path = dst / f"{version}.zip"

with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for rel in members:
        data = (src / rel).read_bytes()
        zi = zipfile.ZipInfo(f"{module}@{version}/{rel}", date_time=(1980, 1, 1, 0, 0, 0))
        zi.create_system = 3
        zi.external_attr = (stat.S_IFREG | 0o644) << 16
        zf.writestr(zi, data)

files = []
for rel in members:
    data = (src / rel).read_bytes()
    files.append(OrderedDict([
        ("path", rel),
        ("size_bytes", len(data)),
        ("sha256", hashlib.sha256(data).hexdigest()),
    ]))

manifest = OrderedDict([
    ("module", module),
    ("version", version),
    ("files", files),
    ("zip_sha256", hashlib.sha256(zip_path.read_bytes()).hexdigest()),
    ("mod_sha256", hashlib.sha256((dst / f"{version}.mod").read_bytes()).hexdigest()),
    ("info_sha256", hashlib.sha256((dst / f"{version}.info").read_bytes()).hexdigest()),
])
(dst / "proxy-manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n")
PY

chmod 0644 "$dst/list" "$dst/$version.info" "$dst/$version.mod" "$dst/$version.zip" "$dst/proxy-manifest.json"
