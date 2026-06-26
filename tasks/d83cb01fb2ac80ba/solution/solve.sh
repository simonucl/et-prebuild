#!/bin/bash
set -euo pipefail

repo=/app/mirror/registry.acme.test/acme/edgeaudit
src=/app/provider-src
archive=terraform-provider-edgeaudit_0.4.2_linux_amd64.zip

rm -rf "$repo"
mkdir -p "$repo"

python3 - <<'PY'
import hashlib
import json
import zipfile
from pathlib import Path

repo = Path("/app/mirror/registry.acme.test/acme/edgeaudit")
src = Path("/app/provider-src")
archive_name = "terraform-provider-edgeaudit_0.4.2_linux_amd64.zip"
archive_path = repo / archive_name

entries = [
    ("terraform-provider-edgeaudit_v0.4.2", 0o755),
    ("LICENSE.txt", 0o644),
]

with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for name, mode in entries:
        zi = zipfile.ZipInfo(name, (2024, 1, 1, 0, 0, 0))
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = (mode & 0xFFFF) << 16
        zf.writestr(zi, (src / name).read_bytes())

zip_bytes = archive_path.read_bytes()
zip_sha = hashlib.sha256(zip_bytes).hexdigest()
zip_size = len(zip_bytes)

(repo / "index.json").write_text(
    json.dumps(
        {"versions": {"0.4.2": {"protocols": ["5.0"]}}},
        separators=(",", ":"),
    )
    + "\n",
    encoding="utf-8",
)

(repo / "0.4.2.json").write_text(
    json.dumps(
        {
            "archives": {
                "linux_amd64": {
                    "url": archive_name,
                    "hashes": [f"zh:{zip_sha}"],
                }
            }
        },
        separators=(",", ":"),
    )
    + "\n",
    encoding="utf-8",
)

(repo / "manifest.json").write_text(
    json.dumps(
        {
            "hostname": "registry.acme.test",
            "namespace": "acme",
            "type": "edgeaudit",
            "version": "0.4.2",
            "platform": "linux_amd64",
            "archive": archive_name,
            "sha256": zip_sha,
            "size": zip_size,
        },
        separators=(",", ":"),
    )
    + "\n",
    encoding="utf-8",
)
PY
