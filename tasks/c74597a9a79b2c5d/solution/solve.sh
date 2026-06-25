#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import base64
import csv
import hashlib
import io
import shutil
import zipfile
from pathlib import Path

root = Path("/home/user/wheel_lab")
src = root / "src"
dist = root / "dist"
simple = root / "simple" / "acme-ledger-export"
wheel_name = "acme_ledger_export-0.4.2-py3-none-any.whl"
wheel_path = dist / wheel_name

dist.mkdir(parents=True, exist_ok=True)
simple.mkdir(parents=True, exist_ok=True)
for child in dist.iterdir():
    if child.is_dir():
        shutil.rmtree(child)
    else:
        child.unlink()

members = [
    ("acme_ledger_export/__init__.py", (src / "acme_ledger_export/__init__.py").read_bytes()),
    ("acme_ledger_export/cli.py", (src / "acme_ledger_export/cli.py").read_bytes()),
    ("acme_ledger_export/schemas/default.json", (src / "acme_ledger_export/schemas/default.json").read_bytes()),
    ("acme_ledger_export-0.4.2.dist-info/METADATA", (
        "Metadata-Version: 2.1\n"
        "Name: acme-ledger-export\n"
        "Version: 0.4.2\n"
        "Summary: Offline ledger export normalizer\n"
        "Requires-Python: >=3.10\n"
    ).encode()),
    ("acme_ledger_export-0.4.2.dist-info/WHEEL", (
        "Wheel-Version: 1.0\n"
        "Generator: terminal-rsi\n"
        "Root-Is-Purelib: true\n"
        "Tag: py3-none-any\n"
    ).encode()),
    ("acme_ledger_export-0.4.2.dist-info/entry_points.txt", (
        "[console_scripts]\n"
        "ledger-export = acme_ledger_export.cli:main\n"
    ).encode()),
]

rows = []
for name, data in members:
    digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode().rstrip("=")
    rows.append([name, f"sha256={digest}", str(len(data))])
rows.append(["acme_ledger_export-0.4.2.dist-info/RECORD", "", ""])
record_text = io.StringIO()
writer = csv.writer(record_text, lineterminator="\n")
writer.writerows(rows)
members.append(("acme_ledger_export-0.4.2.dist-info/RECORD", record_text.getvalue().encode()))

with zipfile.ZipFile(wheel_path, "w") as zf:
    for name, data in members:
        info = zipfile.ZipInfo(name, (2024, 2, 29, 12, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        zf.writestr(info, data)

wheel_sha = hashlib.sha256(wheel_path.read_bytes()).hexdigest()
(dist / "SHA256SUMS").write_text(f"{wheel_sha}  {wheel_name}\n")
(simple / "index.html").write_text(
    "<!DOCTYPE html>\n"
    "<html>\n"
    "  <body>\n"
    f"    <a href=\"../../dist/{wheel_name}#sha256={wheel_sha}\">{wheel_name}</a>\n"
    "  </body>\n"
    "</html>\n"
)
PY
