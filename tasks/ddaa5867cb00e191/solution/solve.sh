#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

root = Path("/app")
src_root = root / "provider-src"
mirror = root / "mirror" / "registry.terraform.io" / "acme" / "edge-router"
version = "1.2.3"
binary_name = f"terraform-provider-edge-router_v{version}_x5"
platforms = ["darwin_arm64", "linux_amd64"]

if mirror.exists():
    shutil.rmtree(mirror)
mirror.mkdir(parents=True)

digests = {}
for platform in platforms:
    source = src_root / platform / binary_name
    zip_name = f"terraform-provider-edge-router_{version}_{platform}.zip"
    zip_path = mirror / zip_name
    info = zipfile.ZipInfo(binary_name, (2024, 3, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = (0o100755 << 16)
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr(info, source.read_bytes(), compress_type=zipfile.ZIP_DEFLATED)
    digests[platform] = hashlib.sha256(zip_path.read_bytes()).hexdigest()

(mirror / "index.json").write_text(json.dumps({"versions": {version: {}}}, separators=(",", ":")) + "\n")

version_doc = {"archives": {}}
for platform in platforms:
    zip_name = f"terraform-provider-edge-router_{version}_{platform}.zip"
    version_doc["archives"][platform] = {
        "url": zip_name,
        "hashes": [f"zh:{digests[platform]}"],
    }
(mirror / f"{version}.json").write_text(json.dumps(version_doc, separators=(",", ":")) + "\n")

lines = []
for platform in platforms:
    zip_name = f"terraform-provider-edge-router_{version}_{platform}.zip"
    lines.append(f"{digests[platform]}  {zip_name}")
(mirror / "SHA256SUMS").write_text("\n".join(lines) + "\n")
PY
