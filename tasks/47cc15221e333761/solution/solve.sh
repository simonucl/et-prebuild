#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import base64
import csv
import hashlib
import io
import json
import os
import shutil
import zipfile
from pathlib import Path

SRC = Path("/app/pkg-src")
OUT = Path("/app/simple")
PKG = "acme_edge_sentinel"
DIST = "acme_edge_sentinel-0.6.0.dist-info"
WHEEL = "acme_edge_sentinel-0.6.0-py3-none-any.whl"
PROJECT = "acme-edge-sentinel"
TS = (2024, 1, 1, 0, 0, 0)

metadata = (
    "Metadata-Version: 2.1\n"
    "Name: acme-edge-sentinel\n"
    "Version: 0.6.0\n"
    "Summary: Offline edge policy sentinel\n"
    "Requires-Python: >=3.10\n"
    "Classifier: Programming Language :: Python :: 3\n"
    "\n"
)
wheel_meta = (
    "Wheel-Version: 1.0\n"
    "Generator: terminal-rsi\n"
    "Root-Is-Purelib: true\n"
    "Tag: py3-none-any\n"
    "\n"
)
entry_points = (
    "[console_scripts]\n"
    "edge-sentinel = acme_edge_sentinel.cli:main\n"
)

def digest(data: bytes) -> str:
    return base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode().rstrip("=")

members = [
    (f"{PKG}/__init__.py", (SRC / PKG / "__init__.py").read_bytes()),
    (f"{PKG}/rules.py", (SRC / PKG / "rules.py").read_bytes()),
    (f"{PKG}/cli.py", (SRC / PKG / "cli.py").read_bytes()),
    (f"{DIST}/METADATA", metadata.encode()),
    (f"{DIST}/WHEEL", wheel_meta.encode()),
    (f"{DIST}/entry_points.txt", entry_points.encode()),
]

record_rows = [[name, f"sha256={digest(data)}", str(len(data))] for name, data in members]
record_rows.append([f"{DIST}/RECORD", "", ""])
record_io = io.StringIO(newline="")
csv.writer(record_io, lineterminator="\n").writerows(record_rows)
members.append((f"{DIST}/RECORD", record_io.getvalue().encode()))

wheel_io = io.BytesIO()
with zipfile.ZipFile(wheel_io, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for name, data in members:
        info = zipfile.ZipInfo(name, TS)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        zf.writestr(info, data)
wheel_bytes = wheel_io.getvalue()
meta_bytes = metadata.encode()

if OUT.exists():
    shutil.rmtree(OUT)
project_dir = OUT / PROJECT
project_dir.mkdir(parents=True)

(project_dir / WHEEL).write_bytes(wheel_bytes)
(project_dir / f"{WHEEL}.metadata").write_bytes(meta_bytes)

wheel_hash = hashlib.sha256(wheel_bytes).hexdigest()
meta_hash = hashlib.sha256(meta_bytes).hexdigest()

project_index = (
    "<!DOCTYPE html>\n"
    "<html><body>\n"
    f'<a href="{WHEEL}#sha256={wheel_hash}" data-dist-info-metadata="sha256={meta_hash}">{WHEEL}</a>\n'
    "</body></html>\n"
)
(project_dir / "index.html").write_text(project_index)

root_index = (
    "<!DOCTYPE html>\n"
    "<html><body>\n"
    '<a href="acme-edge-sentinel/">acme-edge-sentinel</a>\n'
    "</body></html>\n"
)
(OUT / "index.html").write_text(root_index)

manifest = {
    "name": "acme-edge-sentinel",
    "normalized": "acme-edge-sentinel",
    "version": "0.6.0",
    "files": {
        WHEEL: f"sha256:{wheel_hash}",
        f"{WHEEL}.metadata": f"sha256:{meta_hash}",
        "index.html": f"sha256:{hashlib.sha256(project_index.encode()).hexdigest()}",
    },
}
(project_dir / "repo-manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n")
PY
