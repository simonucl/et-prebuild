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

root = Path("/app")
src = root / "provider-src"
mirror = root / "mirror" / "registry.terraform.io" / "acme" / "edgecache"
version = "1.2.0"
platforms = ["linux_amd64", "linux_arm64"]
binary_name = f"terraform-provider-edgecache_v{version}_x5"
expected_entries = ["LICENSE.txt", "README.md", binary_name]

def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)

def read_exact(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except FileNotFoundError:
        fail(f"missing required file: {path}")

expected_index_bytes = b'{"versions":{"1.2.0":{}}}\n'
if read_exact(mirror / "index.json") != expected_index_bytes:
    fail("index.json is not the required compact Terraform mirror index")

try:
    version_doc = json.loads(read_exact(mirror / "1.2.0.json"))
except json.JSONDecodeError as exc:
    fail(f"1.2.0.json is not valid JSON: {exc}")

if set(version_doc.keys()) != {"archives"}:
    fail("1.2.0.json must contain only the archives object")
archives = version_doc["archives"]
if list(archives.keys()) != platforms:
    fail("1.2.0.json platforms are missing, extra, or in the wrong order")

expected_archive_doc = {"archives": {}}

for platform in platforms:
    zip_name = f"terraform-provider-edgecache_{version}_{platform}.zip"
    zip_path = mirror / zip_name
    zip_bytes = read_exact(zip_path)
    digest = hashlib.sha256(zip_bytes).hexdigest()
    expected_archive_doc["archives"][platform] = {
        "url": zip_name,
        "hashes": [f"zh:{digest}"],
    }

    try:
        with zipfile.ZipFile(zip_path) as zf:
            infos = zf.infolist()
            names = [info.filename for info in infos]
            if names != expected_entries:
                fail(f"{zip_name} has wrong member order or file set: {names}")
            for info in infos:
                if info.date_time != (1980, 1, 1, 0, 0, 0):
                    fail(f"{zip_name}:{info.filename} has non-normalized timestamp")
                if info.create_system != 3:
                    fail(f"{zip_name}:{info.filename} was not written with Unix metadata")
                mode = (info.external_attr >> 16) & 0o777
                expected_mode = 0o755 if info.filename == binary_name else 0o644
                if mode != expected_mode:
                    fail(f"{zip_name}:{info.filename} mode is {oct(mode)}, expected {oct(expected_mode)}")
            if zf.read("LICENSE.txt") != (src / "LICENSE.txt").read_bytes():
                fail(f"{zip_name}: LICENSE.txt content does not match source")
            if zf.read("README.md") != (src / "README.md").read_bytes():
                fail(f"{zip_name}: README.md content does not match source")
            if zf.read(binary_name) != (src / platform / binary_name).read_bytes():
                fail(f"{zip_name}: provider binary content does not match {platform} source")
    except zipfile.BadZipFile:
        fail(f"{zip_name} is not a valid ZIP archive")

expected_version_bytes = json.dumps(expected_archive_doc, separators=(",", ":")).encode() + b"\n"
if read_exact(mirror / "1.2.0.json") != expected_version_bytes:
    fail("1.2.0.json content, ordering, URLs, hashes, or trailing newline is incorrect")

expected_files = {
    "index.json",
    "1.2.0.json",
    "terraform-provider-edgecache_1.2.0_linux_amd64.zip",
    "terraform-provider-edgecache_1.2.0_linux_arm64.zip",
}
actual_files = {p.name for p in mirror.iterdir() if p.is_file()}
if actual_files != expected_files:
    fail(f"mirror directory has unexpected file set: {sorted(actual_files)}")
PY

if [ "$?" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
