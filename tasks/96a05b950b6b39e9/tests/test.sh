#!/bin/bash
set -euo pipefail

mkdir -p /logs/verifier

python3 - <<'PY'
from __future__ import annotations

import base64
import hashlib
import os
import stat
import sys
import zipfile
from pathlib import Path

reward = Path("/logs/verifier/reward.txt")

def fail(message: str) -> None:
    print(f"FAIL: {message}")
    reward.write_text("0\n")
    sys.exit(0)

root = Path("/home/user/work/packet_sentinel")
wheel = root / "dist" / "packet_sentinel-1.2.0-py3-none-any.whl"
if not wheel.is_file():
    fail("expected wheel file is missing")

expected_source = {
    "packet_sentinel/__init__.py": '"""Packet Sentinel rule inspection helpers."""\n\n__version__ = "1.2.0"\n',
    "packet_sentinel/cli.py": '''from __future__ import annotations

import argparse
from importlib.resources import files


def load_default_rules() -> str:
    return files("packet_sentinel.rules").joinpath("defaults.toml").read_text()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="packet-sentinel")
    parser.add_argument("--show-defaults", action="store_true")
    args = parser.parse_args(argv)
    if args.show_defaults:
        print(load_default_rules(), end="")
    return 0
''',
    "packet_sentinel/rules/defaults.toml": """[limits]
max_payload_bytes = 4096
max_header_bytes = 1024

[actions]
drop_malformed = true
log_unknown_protocols = true
""",
    "packet_sentinel/py.typed": "",
}

for rel, expected in expected_source.items():
    path = root / rel
    if not path.is_file() or path.read_text() != expected:
        fail(f"source file was modified or is missing: {rel}")

expected_members = [
    "packet_sentinel/__init__.py",
    "packet_sentinel/cli.py",
    "packet_sentinel/rules/defaults.toml",
    "packet_sentinel/py.typed",
    "packet_sentinel-1.2.0.dist-info/METADATA",
    "packet_sentinel-1.2.0.dist-info/WHEEL",
    "packet_sentinel-1.2.0.dist-info/entry_points.txt",
    "packet_sentinel-1.2.0.dist-info/RECORD",
]

try:
    zf = zipfile.ZipFile(wheel)
except zipfile.BadZipFile:
    fail("wheel is not a valid zip file")

with zf:
    names = zf.namelist()
    if names != expected_members:
        fail(f"unexpected wheel members or order: {names!r}")

    for info in zf.infolist():
        if info.compress_type != zipfile.ZIP_DEFLATED:
            fail(f"{info.filename} is not deflated")
        mode = (info.external_attr >> 16) & 0o777
        if mode != 0o644:
            fail(f"{info.filename} has zip permission {oct(mode)}, expected 0644")
        if info.date_time != (2024, 1, 1, 0, 0, 0):
            fail(f"{info.filename} does not use the required stable timestamp")

    expected_payloads = {
        "packet_sentinel/__init__.py": expected_source["packet_sentinel/__init__.py"].encode(),
        "packet_sentinel/cli.py": expected_source["packet_sentinel/cli.py"].encode(),
        "packet_sentinel/rules/defaults.toml": expected_source["packet_sentinel/rules/defaults.toml"].encode(),
        "packet_sentinel/py.typed": b"",
        "packet_sentinel-1.2.0.dist-info/METADATA": b"""Metadata-Version: 2.1
Name: packet-sentinel
Version: 1.2.0
Summary: Internal packet rule inspection helpers
Requires-Python: >=3.10
Description-Content-Type: text/markdown

# Packet Sentinel

Packet Sentinel is an internal example package used for wheel publication drills.
""",
        "packet_sentinel-1.2.0.dist-info/WHEEL": b"""Wheel-Version: 1.0
Generator: trsi-wheelhouse 1.0
Root-Is-Purelib: true
Tag: py3-none-any
""",
        "packet_sentinel-1.2.0.dist-info/entry_points.txt": b"""[console_scripts]
packet-sentinel = packet_sentinel.cli:main
""",
    }

    for name, expected in expected_payloads.items():
        actual = zf.read(name)
        if actual != expected:
            fail(f"{name} content is incorrect")

    expected_rows = []
    for name in expected_members[:-1]:
        payload = expected_payloads[name]
        digest = base64.urlsafe_b64encode(hashlib.sha256(payload).digest()).decode().rstrip("=")
        expected_rows.append(f"{name},sha256={digest},{len(payload)}")
    expected_rows.append("packet_sentinel-1.2.0.dist-info/RECORD,,")
    expected_record = "\n".join(expected_rows) + "\n"
    if zf.read("packet_sentinel-1.2.0.dist-info/RECORD").decode() != expected_record:
        fail("RECORD paths, hashes, sizes, order, or self-entry are incorrect")

reward.write_text("1\n")
print("ok")
PY
