#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import tarfile

source = Path("/home/user/src/widget")
release = Path("/home/user/release")
release.mkdir(parents=True, exist_ok=True)

epoch = 1704067200
prefix = "widget-2.4.1"
files = [
    ("LICENSE", 0o644),
    ("README.md", 0o644),
    ("docs/usage.md", 0o644),
    ("pyproject.toml", 0o644),
    ("scripts/widget-smoke", 0o755),
    ("src/widget/__init__.py", 0o644),
    ("src/widget/core.py", 0o644),
    ("src/widget/data/defaults.toml", 0o644),
]

tar_buffer = io.BytesIO()
manifest_files = []
with tarfile.open(fileobj=tar_buffer, mode="w", format=tarfile.USTAR_FORMAT) as tar:
    for rel, mode in files:
        data = (source / rel).read_bytes()
        info = tarfile.TarInfo(f"{prefix}/{rel}")
        info.size = len(data)
        info.mode = mode
        info.mtime = epoch
        info.uid = 0
        info.gid = 0
        info.uname = ""
        info.gname = ""
        tar.addfile(info, io.BytesIO(data))
        manifest_files.append({
            "path": rel,
            "mode": f"{mode:04o}",
            "size_bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        })

archive_path = release / "widget-2.4.1.tar.gz"
with archive_path.open("wb") as raw:
    with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
        gz.write(tar_buffer.getvalue())

archive_bytes = archive_path.read_bytes()
archive_sha = hashlib.sha256(archive_bytes).hexdigest()
(release / "SHA256SUMS").write_text(
    f"{archive_sha}  widget-2.4.1.tar.gz\n",
    encoding="utf-8",
)

manifest = {
    "name": "widget",
    "version": "2.4.1",
    "source_date_epoch": epoch,
    "archive": "widget-2.4.1.tar.gz",
    "sha256": archive_sha,
    "size_bytes": len(archive_bytes),
    "files": manifest_files,
}
(release / "widget-2.4.1.manifest.json").write_text(
    json.dumps(manifest, separators=(",", ":")) + "\n",
    encoding="utf-8",
)
PY
