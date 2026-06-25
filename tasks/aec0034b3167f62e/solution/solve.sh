#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import hashlib
import json
import stat
import zipfile
from pathlib import Path

root = Path("/app")
src = root / "provider-src"
mirror = root / "mirror" / "registry.terraform.io" / "acme" / "edgecache"
mirror.mkdir(parents=True, exist_ok=True)

version = "1.2.0"
platforms = ["linux_amd64", "linux_arm64"]
zip_names = {}

fixed_time = (1980, 1, 1, 0, 0, 0)

def add_file(zf: zipfile.ZipFile, arcname: str, path: Path, mode: int) -> None:
    info = zipfile.ZipInfo(arcname, fixed_time)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = (stat.S_IFREG | mode) << 16
    zf.writestr(info, path.read_bytes())

for platform in platforms:
    zip_name = f"terraform-provider-edgecache_{version}_{platform}.zip"
    zip_path = mirror / zip_name
    binary = src / platform / f"terraform-provider-edgecache_v{version}_x5"
    with zipfile.ZipFile(zip_path, "w") as zf:
        add_file(zf, "LICENSE.txt", src / "LICENSE.txt", 0o644)
        add_file(zf, "README.md", src / "README.md", 0o644)
        add_file(zf, f"terraform-provider-edgecache_v{version}_x5", binary, 0o755)
    zip_names[platform] = zip_name

(mirror / "index.json").write_text(
    json.dumps({"versions": {version: {}}}, separators=(",", ":")) + "\n",
    encoding="utf-8",
)

archives = {}
for platform in platforms:
    zip_name = zip_names[platform]
    digest = hashlib.sha256((mirror / zip_name).read_bytes()).hexdigest()
    archives[platform] = {"url": zip_name, "hashes": [f"zh:{digest}"]}

(mirror / f"{version}.json").write_text(
    json.dumps({"archives": archives}, separators=(",", ":")) + "\n",
    encoding="utf-8",
)
PY
