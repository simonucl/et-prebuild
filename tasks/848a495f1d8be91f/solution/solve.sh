#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import gzip
import hashlib
import io
import json
import os
import shutil
import stat
import tarfile
from pathlib import Path

root = Path("/app")
src = root / "rootfs"
oci = root / "oci"
blobdir = oci / "blobs" / "sha256"
fixed_mtime = 1704067200
created = "2024-01-01T00:00:00Z"

entries = [
    ("dir", "etc", 0o755, None),
    ("dir", "etc/audit-agent", 0o755, None),
    ("file", "etc/audit-agent/config.yaml", 0o640, src / "etc/audit-agent/config.yaml"),
    ("symlink", "etc/audit-agent/current.yaml", 0o777, "config.yaml"),
    ("dir", "usr", 0o755, None),
    ("dir", "usr/local", 0o755, None),
    ("dir", "usr/local/bin", 0o755, None),
    ("file", "usr/local/bin/audit-agent", 0o755, src / "usr/local/bin/audit-agent"),
    ("dir", "var", 0o755, None),
    ("dir", "var/lib", 0o755, None),
    ("dir", "var/lib/audit-agent", 0o755, None),
    ("file", "var/lib/audit-agent/state.json", 0o644, src / "var/lib/audit-agent/state.json"),
]

def json_bytes(obj):
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n"

def digest(data):
    return hashlib.sha256(data).hexdigest()

def add_entry(tf, kind, name, mode, payload):
    info = tarfile.TarInfo(name)
    info.uid = 0
    info.gid = 0
    info.uname = "root"
    info.gname = "root"
    info.mtime = fixed_mtime
    info.mode = mode
    if kind == "dir":
        info.type = tarfile.DIRTYPE
        info.size = 0
        tf.addfile(info)
    elif kind == "symlink":
        info.type = tarfile.SYMTYPE
        info.linkname = payload
        info.size = 0
        tf.addfile(info)
    else:
        data = payload.read_bytes()
        info.type = tarfile.REGTYPE
        info.size = len(data)
        tf.addfile(info, io.BytesIO(data))

tar_buffer = io.BytesIO()
with tarfile.open(fileobj=tar_buffer, mode="w", format=tarfile.USTAR_FORMAT) as tf:
    for entry in entries:
        add_entry(tf, *entry)
tar_bytes = tar_buffer.getvalue()
diff_id = digest(tar_bytes)

gz_buffer = io.BytesIO()
with gzip.GzipFile(filename="", mode="wb", fileobj=gz_buffer, mtime=fixed_mtime, compresslevel=9) as gz:
    gz.write(tar_bytes)
layer_bytes = gz_buffer.getvalue()
layer_digest = digest(layer_bytes)

config = {
    "architecture": "amd64",
    "os": "linux",
    "created": created,
    "rootfs": {"type": "layers", "diff_ids": [f"sha256:{diff_id}"]},
    "config": {
        "Env": ["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"],
        "Entrypoint": ["/usr/local/bin/audit-agent"],
    },
}
config_bytes = json_bytes(config)
config_digest = digest(config_bytes)

manifest = {
    "schemaVersion": 2,
    "mediaType": "application/vnd.oci.image.manifest.v1+json",
    "config": {
        "mediaType": "application/vnd.oci.image.config.v1+json",
        "digest": f"sha256:{config_digest}",
        "size": len(config_bytes),
    },
    "layers": [
        {
            "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
            "digest": f"sha256:{layer_digest}",
            "size": len(layer_bytes),
            "annotations": {"org.opencontainers.image.title": "rootfs.tar.gz"},
        }
    ],
}
manifest_bytes = json_bytes(manifest)
manifest_digest = digest(manifest_bytes)

index = {
    "schemaVersion": 2,
    "manifests": [
        {
            "mediaType": "application/vnd.oci.image.manifest.v1+json",
            "digest": f"sha256:{manifest_digest}",
            "size": len(manifest_bytes),
            "platform": {"architecture": "amd64", "os": "linux"},
            "annotations": {"org.opencontainers.image.ref.name": "audit-agent:2.4.1"},
        }
    ],
}

if oci.exists():
    for child in oci.iterdir():
        if child.name != "blobs":
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
if blobdir.exists():
    shutil.rmtree(blobdir)
blobdir.mkdir(parents=True, exist_ok=True)

(oci / "oci-layout").write_bytes(json_bytes({"imageLayoutVersion": "1.0.0"}))
(oci / "index.json").write_bytes(json_bytes(index))
(blobdir / manifest_digest).write_bytes(manifest_bytes)
(blobdir / config_digest).write_bytes(config_bytes)
(blobdir / layer_digest).write_bytes(layer_bytes)
PY
