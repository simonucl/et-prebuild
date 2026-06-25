#!/bin/bash
set -euo pipefail

python3 <<'PY'
import gzip
import hashlib
import json
import os
import shutil
import tarfile
from io import BytesIO
from pathlib import Path

root = Path(os.environ.get("ROOT_PREFIX", "/"))
stage = root / "home/user/oci-stage"
rootfs = stage / "rootfs"
out = root / "home/user/oci-export/acme-cache_1.2.0"
blobs = out / "blobs" / "sha256"

if out.exists():
    shutil.rmtree(out)
blobs.mkdir(parents=True)

entries = [
    "etc",
    "etc/acme-cache",
    "etc/acme-cache/config.yaml",
    "etc/acme-cache/current",
    "usr",
    "usr/local",
    "usr/local/bin",
    "usr/local/bin/acme-cache",
    "var",
    "var/lib",
    "var/lib/acme-cache",
    "var/lib/acme-cache/seed.txt",
]

tar_buf = BytesIO()
with tarfile.open(fileobj=tar_buf, mode="w", format=tarfile.PAX_FORMAT) as tf:
    for name in entries:
        src = rootfs / name
        st = src.lstat()
        info = tarfile.TarInfo(name)
        info.uid = 0
        info.gid = 0
        info.uname = ""
        info.gname = ""
        info.mtime = 1704067200
        if src.is_symlink():
            info.type = tarfile.SYMTYPE
            info.mode = 0o777
            info.linkname = os.readlink(src)
            info.size = 0
            tf.addfile(info)
        elif src.is_dir():
            info.type = tarfile.DIRTYPE
            info.mode = 0o755
            info.size = 0
            tf.addfile(info)
        else:
            info.type = tarfile.REGTYPE
            info.mode = 0o755 if name == "usr/local/bin/acme-cache" else 0o644
            data = src.read_bytes()
            info.size = len(data)
            tf.addfile(info, BytesIO(data))

layer_plain = tar_buf.getvalue()
diff_id = hashlib.sha256(layer_plain).hexdigest()
gz_buf = BytesIO()
with gzip.GzipFile(filename="", mode="wb", fileobj=gz_buf, mtime=0) as gz:
    gz.write(layer_plain)
layer_blob = gz_buf.getvalue()
layer_digest = hashlib.sha256(layer_blob).hexdigest()

meta = json.loads((stage / "image-meta.json").read_text(encoding="utf-8"))
config_obj = {
    "created": meta["created"],
    "architecture": meta["architecture"],
    "os": meta["os"],
    "config": {
        "Env": ["PATH=/usr/local/bin:/usr/bin:/bin"],
        "Cmd": ["/usr/local/bin/acme-cache"],
    },
    "rootfs": {
        "type": "layers",
        "diff_ids": [f"sha256:{diff_id}"],
    },
    "history": [
        {
            "created": meta["created"],
            "created_by": "manual offline rootfs import",
        }
    ],
}
config_blob = json.dumps(config_obj, separators=(",", ":")).encode() + b"\n"
config_digest = hashlib.sha256(config_blob).hexdigest()

manifest_obj = {
    "schemaVersion": 2,
    "mediaType": "application/vnd.oci.image.manifest.v1+json",
    "config": {
        "mediaType": "application/vnd.oci.image.config.v1+json",
        "digest": f"sha256:{config_digest}",
        "size": len(config_blob),
    },
    "layers": [
        {
            "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
            "digest": f"sha256:{layer_digest}",
            "size": len(layer_blob),
        }
    ],
    "annotations": {
        "org.opencontainers.image.version": "1.2.0",
    },
}
manifest_blob = json.dumps(manifest_obj, separators=(",", ":")).encode() + b"\n"
manifest_digest = hashlib.sha256(manifest_blob).hexdigest()

(blobs / config_digest).write_bytes(config_blob)
(blobs / layer_digest).write_bytes(layer_blob)
(blobs / manifest_digest).write_bytes(manifest_blob)

index_obj = {
    "schemaVersion": 2,
    "manifests": [
        {
            "mediaType": "application/vnd.oci.image.manifest.v1+json",
            "digest": f"sha256:{manifest_digest}",
            "size": len(manifest_blob),
            "annotations": {
                "org.opencontainers.image.ref.name": meta["tag"],
            },
        }
    ],
}
(out / "index.json").write_bytes(json.dumps(index_obj, separators=(",", ":")).encode() + b"\n")
(out / "oci-layout").write_text('{"imageLayoutVersion":"1.0.0"}\n', encoding="utf-8")
PY
