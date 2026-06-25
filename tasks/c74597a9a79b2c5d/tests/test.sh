#!/bin/bash
set -uo pipefail

mkdir -p /logs/verifier
reward=0

if python3 - <<'PY'
import base64
import csv
import hashlib
import io
import sys
import zipfile
from pathlib import Path

root = Path("/home/user/wheel_lab")
src = root / "src"
dist = root / "dist"
simple = root / "simple" / "acme-ledger-export"
wheel_name = "acme_ledger_export-0.4.2-py3-none-any.whl"
wheel_path = dist / wheel_name
sha_path = dist / "SHA256SUMS"
index_path = simple / "index.html"

expected_names = [
    "acme_ledger_export/__init__.py",
    "acme_ledger_export/cli.py",
    "acme_ledger_export/schemas/default.json",
    "acme_ledger_export-0.4.2.dist-info/METADATA",
    "acme_ledger_export-0.4.2.dist-info/WHEEL",
    "acme_ledger_export-0.4.2.dist-info/entry_points.txt",
    "acme_ledger_export-0.4.2.dist-info/RECORD",
]

expected_text = {
    "acme_ledger_export/__init__.py": (src / "acme_ledger_export/__init__.py").read_bytes(),
    "acme_ledger_export/cli.py": (src / "acme_ledger_export/cli.py").read_bytes(),
    "acme_ledger_export/schemas/default.json": (src / "acme_ledger_export/schemas/default.json").read_bytes(),
    "acme_ledger_export-0.4.2.dist-info/METADATA": (
        "Metadata-Version: 2.1\n"
        "Name: acme-ledger-export\n"
        "Version: 0.4.2\n"
        "Summary: Offline ledger export normalizer\n"
        "Requires-Python: >=3.10\n"
    ).encode(),
    "acme_ledger_export-0.4.2.dist-info/WHEEL": (
        "Wheel-Version: 1.0\n"
        "Generator: terminal-rsi\n"
        "Root-Is-Purelib: true\n"
        "Tag: py3-none-any\n"
    ).encode(),
    "acme_ledger_export-0.4.2.dist-info/entry_points.txt": (
        "[console_scripts]\n"
        "ledger-export = acme_ledger_export.cli:main\n"
    ).encode(),
}

def fail(message):
    print(message)
    sys.exit(1)

if not dist.is_dir():
    fail("dist directory is missing")
if not wheel_path.is_file():
    fail("wheel file is missing")
if not sha_path.is_file():
    fail("SHA256SUMS is missing")
if not index_path.is_file():
    fail("simple index is missing")

dist_entries = sorted(p.name for p in dist.iterdir())
if dist_entries != ["SHA256SUMS", wheel_name]:
    fail(f"dist directory contains unexpected entries: {dist_entries}")

try:
    with zipfile.ZipFile(wheel_path, "r") as zf:
        infos = zf.infolist()
        names = [info.filename for info in infos]
        if names != expected_names:
            fail(f"unexpected wheel members or order: {names}")
        if any(name.endswith("/") for name in names):
            fail("wheel must not contain directory entries")
        for info in infos:
            if info.date_time != (2024, 2, 29, 12, 0, 0):
                fail(f"{info.filename} has non-normalized timestamp {info.date_time}")
            if info.compress_type != zipfile.ZIP_DEFLATED:
                fail(f"{info.filename} is not deflated")
            mode = (info.external_attr >> 16) & 0o7777
            if mode != 0o644:
                fail(f"{info.filename} has mode {oct(mode)}, expected 0644")
        contents = {name: zf.read(name) for name in names}
except zipfile.BadZipFile:
    fail("wheel is not a valid zip archive")

for name, data in expected_text.items():
    if contents.get(name) != data:
        fail(f"{name} content is incorrect")
    if not data.endswith(b"\n") or data.endswith(b"\n\n"):
        fail(f"{name} must end with exactly one newline")

record_bytes = contents["acme_ledger_export-0.4.2.dist-info/RECORD"]
if not record_bytes.endswith(b"\n") or record_bytes.endswith(b"\n\n"):
    fail("RECORD must end with exactly one newline")
try:
    rows = list(csv.reader(io.StringIO(record_bytes.decode("utf-8"), newline="")))
except Exception as exc:
    fail(f"RECORD is not parseable CSV: {exc}")

expected_rows = []
for name in expected_names[:-1]:
    data = contents[name]
    digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode().rstrip("=")
    expected_rows.append([name, f"sha256={digest}", str(len(data))])
expected_rows.append(["acme_ledger_export-0.4.2.dist-info/RECORD", "", ""])
if rows != expected_rows:
    fail("RECORD rows, hashes, sizes, or order are incorrect")

wheel_sha = hashlib.sha256(wheel_path.read_bytes()).hexdigest()
expected_sha_line = f"{wheel_sha}  {wheel_name}\n"
if sha_path.read_text() != expected_sha_line:
    fail("SHA256SUMS has the wrong digest, spacing, filename, or newline")

expected_index = (
    "<!DOCTYPE html>\n"
    "<html>\n"
    "  <body>\n"
    f"    <a href=\"../../dist/{wheel_name}#sha256={wheel_sha}\">{wheel_name}</a>\n"
    "  </body>\n"
    "</html>\n"
)
if index_path.read_text() != expected_index:
    fail("simple index content is incorrect")

print("all checks passed")
PY
then
  reward=1
fi

echo "$reward" > /logs/verifier/reward.txt
