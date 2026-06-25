#!/bin/bash
set -u

mkdir -p /logs/verifier

python3 - <<'PY'
import hashlib
import json
import stat
import sys
import zipfile
from pathlib import Path

src = Path("/app/pkg-src/package")
repo = Path("/app/repo")
zip_path = repo / "dist" / "acme-edge-probe-2.3.1.zip"
packages_path = repo / "packages.json"
expected_entries = [
    "composer.json",
    "LICENSE",
    "README.md",
    "bin/edge-probe",
    "src/Acme/EdgeProbe.php",
    "src/Acme/Console/ProbeCommand.php",
]

def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)

if not packages_path.is_file():
    fail("missing /app/repo/packages.json")
if not zip_path.is_file():
    fail("missing /app/repo/dist/acme-edge-probe-2.3.1.zip")

top_entries = sorted(p.name for p in repo.iterdir())
if top_entries != ["dist", "packages.json"]:
    fail(f"/app/repo has unexpected top-level entries: {top_entries}")
dist_entries = sorted(p.name for p in (repo / "dist").iterdir())
if dist_entries != ["acme-edge-probe-2.3.1.zip"]:
    fail(f"/app/repo/dist has unexpected entries: {dist_entries}")

zip_bytes = zip_path.read_bytes()
if len(zip_bytes) < 100:
    fail("dist ZIP is too small to be valid")

try:
    with zipfile.ZipFile(zip_path) as zf:
        infos = zf.infolist()
        names = [info.filename for info in infos]
        if names != expected_entries:
            fail(f"ZIP entries are missing, extra, or in the wrong order: {names}")
        for info in infos:
            if info.is_dir():
                fail(f"ZIP must not contain directory entry {info.filename}")
            if info.date_time != (1980, 1, 1, 0, 0, 0):
                fail(f"{info.filename} timestamp is not normalized")
            if info.create_system != 3:
                fail(f"{info.filename} was not written with Unix metadata")
            if info.compress_type != zipfile.ZIP_DEFLATED:
                fail(f"{info.filename} is not deflated")
            mode = (info.external_attr >> 16) & 0o777
            expected_mode = 0o755 if info.filename == "bin/edge-probe" else 0o644
            if mode != expected_mode:
                fail(f"{info.filename} mode is {oct(mode)}, expected {oct(expected_mode)}")
            if zf.read(info.filename) != (src / info.filename).read_bytes():
                fail(f"{info.filename} content does not match the package source")
except zipfile.BadZipFile:
    fail("dist artifact is not a valid ZIP")

shasum = hashlib.sha1(zip_bytes).hexdigest()
expected_packages = {
    "packages": {
        "acme/edge-probe": {
            "2.3.1": {
                "name": "acme/edge-probe",
                "version": "2.3.1",
                "type": "library",
                "dist": {
                    "type": "zip",
                    "url": "dist/acme-edge-probe-2.3.1.zip",
                    "shasum": shasum,
                },
                "autoload": {
                    "psr-4": {
                        "Acme\\EdgeProbe\\": "src/Acme/",
                    },
                },
                "bin": ["bin/edge-probe"],
                "require": {"php": ">=8.1"},
            },
        },
    },
}
expected_packages_bytes = json.dumps(expected_packages, separators=(",", ":")).encode() + b"\n"
if packages_path.read_bytes() != expected_packages_bytes:
    try:
        json.loads(packages_path.read_text())
    except Exception as exc:
        fail(f"packages.json is not valid JSON: {exc}")
    fail("packages.json content, key order, shasum, minification, or trailing newline is incorrect")
PY

if [ "$?" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
