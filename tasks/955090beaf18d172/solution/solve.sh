#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import gzip
import hashlib
import io
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

root = Path("/home/user/oci-dual")
basefs = root / "basefs"
patchfs = root / "patchfs"
image = root / "image"
blobdir = image / "blobs" / "sha256"
created = "2025-02-14T12:00:00Z"
mtime = "@1739534400"

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def write_blob(data: bytes) -> tuple[str, int]:
    digest = sha256(data)
    (blobdir / digest).write_bytes(data)
    return "sha256:" + digest, len(data)

def minjson(obj) -> bytes:
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False).encode() + b"\n"

def tar_tree(path: Path) -> bytes:
    return subprocess.check_output(
        [
            "tar",
            "--sort=name",
            f"--mtime={mtime}",
            "--owner=0",
            "--group=0",
            "--numeric-owner",
            "--pax-option=delete=atime,delete=ctime",
            "-cf",
            "-",
            ".",
        ],
        cwd=path,
    )

def gz(data: bytes) -> bytes:
    out = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=out, mtime=0, compresslevel=9) as fh:
        fh.write(data)
    return out.getvalue()

shutil.rmtree(image, ignore_errors=True)
blobdir.mkdir(parents=True, exist_ok=True)
(image / "oci-layout").write_bytes(b'{"imageLayoutVersion":"1.0.0"}\n')

base_tar = tar_tree(basefs)
base_layer = gz(base_tar)
base_digest, base_size = write_blob(base_layer)
base_diff = "sha256:" + sha256(base_tar)

with tempfile.TemporaryDirectory() as td:
    update_root = Path(td) / "update"
    shutil.copytree(patchfs, update_root, symlinks=True)
    whiteout = update_root / "etc/netprobe/.wh.defaults.yaml"
    whiteout.write_bytes(b"")
    os.chmod(whiteout, 0o600)
    update_tar = tar_tree(update_root)

update_layer = gz(update_tar)
update_digest, update_size = write_blob(update_layer)
update_diff = "sha256:" + sha256(update_tar)

config = {
    "created": created,
    "architecture": "amd64",
    "os": "linux",
    "config": {
        "Entrypoint": ["/usr/local/bin/netprobe"],
        "Env": ["NETPROBE_CONFIG=/etc/netprobe/config.yaml"],
        "WorkingDir": "/var/lib/netprobe",
        "Labels": {
            "org.opencontainers.image.title": "netprobe",
            "org.opencontainers.image.version": "2.1.0",
        },
    },
    "rootfs": {"type": "layers", "diff_ids": [base_diff, update_diff]},
    "history": [
        {"created": created, "created_by": "import basefs"},
        {"created": created, "created_by": "apply offline patch"},
    ],
}
config_bytes = minjson(config)
config_digest, config_size = write_blob(config_bytes)

manifest = {
    "schemaVersion": 2,
    "mediaType": "application/vnd.oci.image.manifest.v1+json",
    "config": {
        "mediaType": "application/vnd.oci.image.config.v1+json",
        "digest": config_digest,
        "size": config_size,
    },
    "layers": [
        {
            "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
            "digest": base_digest,
            "size": base_size,
        },
        {
            "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
            "digest": update_digest,
            "size": update_size,
        },
    ],
}
manifest_bytes = minjson(manifest)
manifest_digest, manifest_size = write_blob(manifest_bytes)

index = {
    "schemaVersion": 2,
    "mediaType": "application/vnd.oci.image.index.v1+json",
    "manifests": [
        {
            "mediaType": "application/vnd.oci.image.manifest.v1+json",
            "digest": manifest_digest,
            "size": manifest_size,
            "platform": {"architecture": "amd64", "os": "linux"},
            "annotations": {"org.opencontainers.image.ref.name": "netprobe:2.1.0-offline"},
        }
    ],
}
(image / "index.json").write_bytes(minjson(index))
PY
