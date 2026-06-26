#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import gzip
import hashlib
import io
import json
import shutil
import tarfile
from pathlib import Path

src = Path("/app/collection-src/acme/edge_ops")
out = Path("/app/galaxy")
artifact_rel = Path("artifacts/acme-edge_ops-1.2.3.tar.gz")
artifact = out / artifact_rel
payload_paths = [
    "README.md",
    "LICENSE",
    "docs/usage.md",
    "plugins/module_utils/client.py",
    "plugins/modules/edge_status.py",
    "roles/edge_agent/tasks/main.yml",
]
mtime = 1717200000

if out.exists():
    shutil.rmtree(out)
(out / "artifacts").mkdir(parents=True)

def sha256(data):
    return hashlib.sha256(data).hexdigest()

payload = {name: (src / name).read_bytes() for name in payload_paths}

files_entries = []
for name in payload_paths:
    data = payload[name]
    files_entries.append({
        "name": name,
        "ftype": "file",
        "chksum_type": "sha256",
        "chksum_sha256": sha256(data),
        "size": len(data),
    })

files_json = json.dumps({"files": files_entries, "format": 1}, separators=(",", ":")).encode() + b"\n"

manifest = {
    "collection_info": {
        "namespace": "acme",
        "name": "edge_ops",
        "version": "1.2.3",
        "authors": ["Acme Platform <platform@acme.invalid>"],
        "readme": "README.md",
        "tags": ["edge", "offline", "automation"],
        "description": "Offline automation helpers for Acme edge gateways.",
        "license": [],
        "license_file": "LICENSE",
        "dependencies": {},
        "repository": "https://git.example.invalid/acme/edge-ops",
        "documentation": "https://docs.example.invalid/acme/edge-ops",
        "homepage": "https://example.invalid/acme/edge-ops",
        "issues": "https://git.example.invalid/acme/edge-ops/issues",
    },
    "file_manifest_file": {
        "name": "FILES.json",
        "ftype": "file",
        "chksum_type": "sha256",
        "chksum_sha256": sha256(files_json),
        "format": 1,
    },
    "format": 1,
}
manifest_json = json.dumps(manifest, separators=(",", ":")).encode() + b"\n"

members = [
    ("MANIFEST.json", manifest_json),
    ("FILES.json", files_json),
    *[(name, payload[name]) for name in payload_paths],
]

tar_buf = io.BytesIO()
with tarfile.open(fileobj=tar_buf, mode="w", format=tarfile.PAX_FORMAT) as tf:
    for name, data in members:
        info = tarfile.TarInfo(name)
        info.size = len(data)
        info.mode = 0o644
        info.uid = 0
        info.gid = 0
        info.uname = ""
        info.gname = ""
        info.mtime = mtime
        tf.addfile(info, io.BytesIO(data))

with artifact.open("wb") as raw:
    with gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0) as gz:
        gz.write(tar_buf.getvalue())

artifact_bytes = artifact.read_bytes()
index = {
    "format": 1,
    "namespace": "acme",
    "name": "edge_ops",
    "version": "1.2.3",
    "artifact": str(artifact_rel),
    "sha256": sha256(artifact_bytes),
    "size_bytes": len(artifact_bytes),
    "manifest_sha256": sha256(manifest_json),
    "files_sha256": sha256(files_json),
}
(out / "index.json").write_bytes(json.dumps(index, separators=(",", ":")).encode() + b"\n")
(out / "SHA256SUMS").write_text(f"{sha256(artifact_bytes)}  {artifact_rel}\n")
PY
