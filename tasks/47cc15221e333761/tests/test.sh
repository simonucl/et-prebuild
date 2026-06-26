#!/bin/bash
set -euo pipefail
mkdir -p /logs/verifier

if python3 - <<'PY'
import base64
import csv
import hashlib
import io
import json
import os
import sys
import zipfile
from pathlib import Path

SRC = Path("/app/pkg-src")
OUT = Path("/app/simple")
PKG = "acme_edge_sentinel"
DIST = "acme_edge_sentinel-0.6.0.dist-info"
WHEEL = "acme_edge_sentinel-0.6.0-py3-none-any.whl"
PROJECT = "acme-edge-sentinel"
TS = (2024, 1, 1, 0, 0, 0)

def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)

def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()

def digest(data):
    return base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode().rstrip("=")

def rel_files(root):
    got = []
    for path in root.rglob("*"):
        if path.is_file() or path.is_symlink():
            got.append(path.relative_to(root).as_posix())
        elif path.is_dir():
            continue
    return sorted(got)

expected_files = [
    "acme-edge-sentinel/acme_edge_sentinel-0.6.0-py3-none-any.whl",
    "acme-edge-sentinel/acme_edge_sentinel-0.6.0-py3-none-any.whl.metadata",
    "acme-edge-sentinel/index.html",
    "acme-edge-sentinel/repo-manifest.json",
    "index.html",
]
if rel_files(OUT) != expected_files:
    fail(f"repository file set is wrong: {rel_files(OUT)}")

for protected in [SRC / "pyproject.toml", SRC / PKG / "__init__.py", SRC / PKG / "rules.py", SRC / PKG / "cli.py"]:
    if not protected.exists():
        fail(f"source file was removed: {protected}")

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
members = [
    (f"{PKG}/__init__.py", (SRC / PKG / "__init__.py").read_bytes()),
    (f"{PKG}/rules.py", (SRC / PKG / "rules.py").read_bytes()),
    (f"{PKG}/cli.py", (SRC / PKG / "cli.py").read_bytes()),
    (f"{DIST}/METADATA", metadata.encode()),
    (f"{DIST}/WHEEL", wheel_meta.encode()),
    (f"{DIST}/entry_points.txt", entry_points.encode()),
]
rows = [[name, f"sha256={digest(data)}", str(len(data))] for name, data in members]
rows.append([f"{DIST}/RECORD", "", ""])
record_io = io.StringIO(newline="")
csv.writer(record_io, lineterminator="\n").writerows(rows)
members.append((f"{DIST}/RECORD", record_io.getvalue().encode()))

expected_wheel_io = io.BytesIO()
with zipfile.ZipFile(expected_wheel_io, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for name, data in members:
        info = zipfile.ZipInfo(name, TS)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        zf.writestr(info, data)
expected_wheel = expected_wheel_io.getvalue()

project_dir = OUT / PROJECT
wheel_path = project_dir / WHEEL
meta_path = project_dir / f"{WHEEL}.metadata"

if wheel_path.read_bytes() != expected_wheel:
    try:
        with zipfile.ZipFile(wheel_path) as zf:
            print("Wheel members produced by solver:", zf.namelist())
            for zi in zf.infolist():
                print(f"{zi.filename} {zi.date_time} method={zi.compress_type} mode={oct((zi.external_attr >> 16) & 0o777)}")
    except Exception as exc:
        print(f"Could not inspect solver wheel: {exc}")
    fail("wheel bytes are not the required deterministic artifact")

if meta_path.read_text() != metadata:
    fail(".whl.metadata content is not the exact wheel METADATA")

wheel_hash = sha256_hex(expected_wheel)
meta_hash = sha256_hex(metadata.encode())
expected_project_index = (
    "<!DOCTYPE html>\n"
    "<html><body>\n"
    f'<a href="{WHEEL}#sha256={wheel_hash}" data-dist-info-metadata="sha256={meta_hash}">{WHEEL}</a>\n'
    "</body></html>\n"
)
if (project_dir / "index.html").read_text() != expected_project_index:
    fail("project index.html is not the required PEP 503/658 link page")

expected_root_index = (
    "<!DOCTYPE html>\n"
    "<html><body>\n"
    '<a href="acme-edge-sentinel/">acme-edge-sentinel</a>\n'
    "</body></html>\n"
)
if (OUT / "index.html").read_text() != expected_root_index:
    fail("root index.html is incorrect")

manifest_expected = {
    "name": "acme-edge-sentinel",
    "normalized": "acme-edge-sentinel",
    "version": "0.6.0",
    "files": {
        WHEEL: f"sha256:{wheel_hash}",
        f"{WHEEL}.metadata": f"sha256:{meta_hash}",
        "index.html": f"sha256:{sha256_hex(expected_project_index.encode())}",
    },
}
manifest_text = (project_dir / "repo-manifest.json").read_text()
if manifest_text != json.dumps(manifest_expected, separators=(",", ":")) + "\n":
    fail("repo-manifest.json content, key order, minification, or checksums are wrong")

with zipfile.ZipFile(wheel_path) as zf:
    if zf.namelist() != [name for name, _ in members]:
        fail("wheel member order is wrong")
    for zi in zf.infolist():
        if zi.date_time != TS:
            fail(f"{zi.filename} has non-deterministic timestamp {zi.date_time}")
        if zi.compress_type != zipfile.ZIP_DEFLATED:
            fail(f"{zi.filename} is not deflated")
        if ((zi.external_attr >> 16) & 0o777) != 0o644:
            fail(f"{zi.filename} has wrong file mode")
    record_text = zf.read(f"{DIST}/RECORD").decode()
    if record_text != record_io.getvalue():
        fail("RECORD hashes, sizes, or row order are incorrect")

print("ok")
PY
then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
  exit 1
fi
