#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import hashlib
import json
import stat
import zipfile
from pathlib import Path

src = Path("/app/pkg-src/package")
repo = Path("/app/repo")
dist = repo / "dist"
zip_path = dist / "acme-edge-probe-2.3.1.zip"

dist.mkdir(parents=True, exist_ok=True)
for child in repo.iterdir():
    if child.name not in {"dist"}:
        if child.is_file() or child.is_symlink():
            child.unlink()
for child in dist.iterdir():
    if child.name != zip_path.name:
        if child.is_file() or child.is_symlink():
            child.unlink()

entries = [
    ("composer.json", 0o644),
    ("LICENSE", 0o644),
    ("README.md", 0o644),
    ("bin/edge-probe", 0o755),
    ("src/Acme/EdgeProbe.php", 0o644),
    ("src/Acme/Console/ProbeCommand.php", 0o644),
]

with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for name, mode in entries:
        info = zipfile.ZipInfo(name)
        info.date_time = (1980, 1, 1, 0, 0, 0)
        info.create_system = 3
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = ((stat.S_IFREG | mode) << 16)
        zf.writestr(info, (src / name).read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

shasum = hashlib.sha1(zip_path.read_bytes()).hexdigest()
packages = {
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
(repo / "packages.json").write_bytes(json.dumps(packages, separators=(",", ":")).encode() + b"\n")
PY
