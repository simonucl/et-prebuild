#!/bin/bash
set -euo pipefail

lab=/home/user/tf-mirror-lab
src="$lab/source/provider"
mirror="$lab/mirror/registry.terraform.io/acme/firewall"
zip_name=terraform-provider-acmefirewall_0.4.2_linux_amd64.zip

rm -rf "$mirror"
mkdir -p "$mirror"

python3 - <<'PY'
import hashlib
import json
import zipfile
from pathlib import Path

src = Path("/home/user/tf-mirror-lab/source/provider")
mirror = Path("/home/user/tf-mirror-lab/mirror/registry.terraform.io/acme/firewall")
zip_name = "terraform-provider-acmefirewall_0.4.2_linux_amd64.zip"
zip_path = mirror / zip_name

members = [
    ("terraform-provider-acmefirewall_v0.4.2", 0o755),
    ("LICENSE.txt", 0o644),
]

with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for name, mode in members:
        data = (src / name).read_bytes()
        info = zipfile.ZipInfo(name, date_time=(2024, 6, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = (mode & 0o7777) << 16
        zf.writestr(info, data)

digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()

index = {
    "versions": {
        "0.4.2": {
            "protocols": ["5.0"],
            "platforms": [{"os": "linux", "arch": "amd64"}],
        }
    }
}
(mirror / "index.json").write_text(json.dumps(index, separators=(",", ":")) + "\n")

version = {
    "archives": {
        "linux_amd64": {
            "url": zip_name,
            "hashes": [f"zh:{digest}"],
        }
    }
}
(mirror / "0.4.2.json").write_text(json.dumps(version, separators=(",", ":")) + "\n")
(mirror / "SHA256SUMS").write_text(f"{digest}  {zip_name}\n")
PY
