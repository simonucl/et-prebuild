#!/bin/bash
set -euo pipefail

cd /home/user/work/packet_sentinel
rm -rf dist build-wheel
mkdir -p build-wheel/packet_sentinel/rules build-wheel/packet_sentinel-1.2.0.dist-info dist

cp packet_sentinel/__init__.py build-wheel/packet_sentinel/__init__.py
cp packet_sentinel/cli.py build-wheel/packet_sentinel/cli.py
cp packet_sentinel/rules/defaults.toml build-wheel/packet_sentinel/rules/defaults.toml
cp packet_sentinel/py.typed build-wheel/packet_sentinel/py.typed

cat > build-wheel/packet_sentinel-1.2.0.dist-info/METADATA <<'EOF'
Metadata-Version: 2.1
Name: packet-sentinel
Version: 1.2.0
Summary: Internal packet rule inspection helpers
Requires-Python: >=3.10
Description-Content-Type: text/markdown

# Packet Sentinel

Packet Sentinel is an internal example package used for wheel publication drills.
EOF

cat > build-wheel/packet_sentinel-1.2.0.dist-info/WHEEL <<'EOF'
Wheel-Version: 1.0
Generator: trsi-wheelhouse 1.0
Root-Is-Purelib: true
Tag: py3-none-any
EOF

cat > build-wheel/packet_sentinel-1.2.0.dist-info/entry_points.txt <<'EOF'
[console_scripts]
packet-sentinel = packet_sentinel.cli:main
EOF

python3 - <<'PY'
from __future__ import annotations

import base64
import hashlib
import os
import zipfile
from pathlib import Path

root = Path("build-wheel")
dist_info = "packet_sentinel-1.2.0.dist-info"
members = [
    "packet_sentinel/__init__.py",
    "packet_sentinel/cli.py",
    "packet_sentinel/rules/defaults.toml",
    "packet_sentinel/py.typed",
    f"{dist_info}/METADATA",
    f"{dist_info}/WHEEL",
    f"{dist_info}/entry_points.txt",
]

record_rows: list[str] = []
for name in members:
    payload = (root / name).read_bytes()
    digest = base64.urlsafe_b64encode(hashlib.sha256(payload).digest()).decode().rstrip("=")
    record_rows.append(f"{name},sha256={digest},{len(payload)}")
record_rows.append(f"{dist_info}/RECORD,,")
(root / dist_info / "RECORD").write_text("\n".join(record_rows) + "\n")
members.append(f"{dist_info}/RECORD")

wheel_path = Path("dist/packet_sentinel-1.2.0-py3-none-any.whl")
with zipfile.ZipFile(wheel_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for name in members:
        info = zipfile.ZipInfo(name, date_time=(2024, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = (0o644 << 16)
        zf.writestr(info, (root / name).read_bytes())
PY

rm -rf build-wheel
