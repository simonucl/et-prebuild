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

ROOT = Path("/app/rootfs")
OCI = Path("/app/oci")
BLOBS = OCI / "blobs" / "sha256"
CREATED = "2024-01-01T00:00:00Z"
MTIME = 1704067200
REF = "registry.example.test/edgecache:1.2.0"

def include(rel: str) -> bool:
    return rel not in {"."} and not (
        rel == "var/cache"
        or rel.startswith("var/cache/")
        or rel == "etc/edgecache/edgecache.toml.tmp"
    )

def iter_entries():
    entries = []
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT).as_posix()
        if include(rel):
            entries.append((rel, path))
    return sorted(entries, key=lambda item: item[0])

def tar_bytes() -> bytes:
    out = io.BytesIO()
    with tarfile.open(fileobj=out, mode="w", format=tarfile.PAX_FORMAT) as tf:
        for rel, path in iter_entries():
            st = path.lstat()
            ti = tarfile.TarInfo(rel)
            ti.uid = ti.gid = 0
            ti.uname = ti.gname = "root"
            ti.mtime = MTIME
            if path.is_symlink():
                ti.type = tarfile.SYMTYPE
                ti.linkname = os.readlink(path)
                ti.mode = 0o777
                ti.size = 0
                tf.addfile(ti)
            elif path.is_dir():
                ti.type = tarfile.DIRTYPE
                ti.mode = 0o755
                ti.size = 0
                tf.addfile(ti)
            elif path.is_file():
                ti.type = tarfile.REGTYPE
                ti.mode = 0o755 if (st.st_mode & stat.S_IXUSR) else 0o644
                data = path.read_bytes()
                ti.size = len(data)
                tf.addfile(ti, io.BytesIO(data))
    return out.getvalue()

def gzip_bytes(data: bytes) -> bytes:
    out = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=out, compresslevel=9, mtime=0) as gz:
        gz.write(data)
    return out.getvalue()

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def json_bytes(obj) -> bytes:
    return (json.dumps(obj, separators=(",", ":"), ensure_ascii=False) + "\n").encode()

def write_blob(data: bytes) -> str:
    h = digest(data)
    (BLOBS / h).write_bytes(data)
    return h

if OCI.exists():
    for child in OCI.iterdir():
        if child.name != "blobs":
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
BLOBS.mkdir(parents=True, exist_ok=True)
for old in BLOBS.iterdir():
    if old.is_file():
        old.unlink()

raw_layer = tar_bytes()
diff_id = digest(raw_layer)
layer = gzip_bytes(raw_layer)
layer_digest = write_blob(layer)

config = {
    "created": CREATED,
    "architecture": "amd64",
    "os": "linux",
    "config": {
        "Entrypoint": ["/usr/local/bin/edgecache"],
        "Env": ["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"],
    },
    "rootfs": {"type": "layers", "diff_ids": [f"sha256:{diff_id}"]},
    "history": [{"created": CREATED, "created_by": "edgecache deterministic rootfs import"}],
}
config_bytes = json_bytes(config)
config_digest = write_blob(config_bytes)

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
            "size": len(layer),
        }
    ],
}
manifest_bytes = json_bytes(manifest)
manifest_digest = write_blob(manifest_bytes)

index = {
    "schemaVersion": 2,
    "mediaType": "application/vnd.oci.image.index.v1+json",
    "manifests": [
        {
            "mediaType": "application/vnd.oci.image.manifest.v1+json",
            "digest": f"sha256:{manifest_digest}",
            "size": len(manifest_bytes),
            "platform": {"architecture": "amd64", "os": "linux"},
            "annotations": {"org.opencontainers.image.ref.name": REF},
        }
    ],
}
(OCI / "index.json").write_bytes(json_bytes(index))
(OCI / "oci-layout").write_bytes(b'{"imageLayoutVersion":"1.0.0"}\n')
PY
