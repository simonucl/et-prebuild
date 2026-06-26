#!/bin/bash
set -u

mkdir -p /logs/verifier

python3 - <<'PY'
import hashlib
import json
import shutil
import sys
import zipfile
from pathlib import Path

root = Path("/app")
src_root = root / "provider-src"
mirror = root / "mirror" / "registry.terraform.io" / "acme" / "edge-router"
version = "1.2.3"
binary_name = f"terraform-provider-edge-router_v{version}_x5"
platforms = ["darwin_arm64", "linux_amd64"]
expected_files = [
    "1.2.3.json",
    "SHA256SUMS",
    "index.json",
    "terraform-provider-edge-router_1.2.3_darwin_arm64.zip",
    "terraform-provider-edge-router_1.2.3_linux_amd64.zip",
]

def fail(message):
    print(f"FAIL: {message}")
    sys.exit(1)

if not mirror.is_dir():
    fail("mirror directory is missing")

actual_files = sorted(p.name for p in mirror.iterdir() if p.is_file())
if actual_files != expected_files:
    fail(f"mirror file set is wrong: {actual_files}")

for platform in platforms:
    source = src_root / platform / binary_name
    if not source.is_file():
        fail(f"source binary is missing: {source}")

expected_digests = {}
for platform in platforms:
    source = src_root / platform / binary_name
    zip_name = f"terraform-provider-edge-router_{version}_{platform}.zip"
    actual_zip = mirror / zip_name
    try:
        with zipfile.ZipFile(actual_zip) as zf:
            infos = zf.infolist()
            if [zi.filename for zi in infos] != [binary_name]:
                fail(f"{zip_name} has wrong members: {[zi.filename for zi in infos]}")
            zi = infos[0]
            if zi.compress_type != zipfile.ZIP_DEFLATED:
                fail(f"{zip_name}:{binary_name} is not deflated")
            if zi.date_time != (2024, 3, 1, 0, 0, 0):
                fail(f"{zip_name}:{binary_name} has wrong timestamp {zi.date_time}")
            if ((zi.external_attr >> 16) & 0o777) != 0o755:
                fail(f"{zip_name}:{binary_name} has wrong unix mode")
            if zf.read(binary_name) != source.read_bytes():
                fail(f"{zip_name}:{binary_name} bytes do not match source")
    except zipfile.BadZipFile as exc:
        fail(f"{zip_name} is not a readable ZIP: {exc}")
    expected_digests[platform] = hashlib.sha256(actual_zip.read_bytes()).hexdigest()

expected_index = json.dumps({"versions": {version: {}}}, separators=(",", ":")) + "\n"
if (mirror / "index.json").read_text() != expected_index:
    fail("index.json content is incorrect")

expected_version_doc = {"archives": {}}
for platform in platforms:
    zip_name = f"terraform-provider-edge-router_{version}_{platform}.zip"
    expected_version_doc["archives"][platform] = {
        "url": zip_name,
        "hashes": [f"zh:{expected_digests[platform]}"],
    }
expected_version = json.dumps(expected_version_doc, separators=(",", ":")) + "\n"
if (mirror / f"{version}.json").read_text() != expected_version:
    fail("1.2.3.json content is incorrect")

expected_sums = ""
for platform in platforms:
    zip_name = f"terraform-provider-edge-router_{version}_{platform}.zip"
    expected_sums += f"{expected_digests[platform]}  {zip_name}\n"
if (mirror / "SHA256SUMS").read_text() != expected_sums:
    fail("SHA256SUMS content is incorrect")

print("ok")
PY

if [ "$?" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
