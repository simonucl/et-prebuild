#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import gzip
import hashlib
import io
import json
import shutil
import stat
import tarfile
from pathlib import Path

root = Path("/app/rootfs")
layout = Path("/app/oci-layout")
blob_dir = layout / "blobs" / "sha256"
created = "2024-06-02T00:00:00Z"
tar_mtime = 1717286400
ref = "registry.example.com/acme/edge-gateway:2.4.1"

if layout.exists():
    for child in layout.iterdir():
        if child.name not in {".keep"}:
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
layout.mkdir(parents=True, exist_ok=True)
blob_dir.mkdir(parents=True, exist_ok=True)

entries = []
for path in root.rglob("*"):
    rel = path.relative_to(root).as_posix()
    if rel == "run" or rel.startswith("run/") or rel == "tmp" or rel.startswith("tmp/"):
        continue
    entries.append((rel, path))
entries.sort(key=lambda item: item[0].encode())

tar_buffer = io.BytesIO()
with tarfile.open(fileobj=tar_buffer, mode="w", format=tarfile.PAX_FORMAT) as tf:
    for rel, path in entries:
        ti = tf.gettarinfo(str(path), arcname=rel)
        ti.uid = 0
        ti.gid = 0
        ti.uname = "root"
        ti.gname = "root"
        ti.mtime = tar_mtime
        if path.is_dir():
            ti.mode = 0o755
            tf.addfile(ti)
        elif path.is_file():
            source_mode = stat.S_IMODE(path.stat().st_mode)
            ti.mode = 0o755 if (source_mode & 0o111) else 0o644
            with path.open("rb") as fh:
                tf.addfile(ti, fh)

tar_bytes = tar_buffer.getvalue()
diff_digest = hashlib.sha256(tar_bytes).hexdigest()

gz_buffer = io.BytesIO()
with gzip.GzipFile(filename="", mode="wb", fileobj=gz_buffer, mtime=0, compresslevel=9) as gz:
    gz.write(tar_bytes)
layer_bytes = gz_buffer.getvalue()
layer_digest = hashlib.sha256(layer_bytes).hexdigest()

config_doc = {
    "architecture": "amd64",
    "os": "linux",
    "created": created,
    "config": {
        "Env": ["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"],
        "Entrypoint": ["/usr/local/bin/edge-gateway"],
    },
    "rootfs": {
        "type": "layers",
        "diff_ids": [f"sha256:{diff_digest}"],
    },
}
config_bytes = json.dumps(config_doc, separators=(",", ":")).encode() + b"\n"
config_digest = hashlib.sha256(config_bytes).hexdigest()

manifest_doc = {
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
        }
    ],
}
manifest_bytes = json.dumps(manifest_doc, separators=(",", ":")).encode() + b"\n"
manifest_digest = hashlib.sha256(manifest_bytes).hexdigest()

index_doc = {
    "schemaVersion": 2,
    "manifests": [
        {
            "mediaType": "application/vnd.oci.image.manifest.v1+json",
            "digest": f"sha256:{manifest_digest}",
            "size": len(manifest_bytes),
            "platform": {"architecture": "amd64", "os": "linux"},
            "annotations": {"org.opencontainers.image.ref.name": ref},
        }
    ],
}
index_bytes = json.dumps(index_doc, separators=(",", ":")).encode() + b"\n"

(layout / "oci-layout").write_bytes(b'{"imageLayoutVersion":"1.0.0"}\n')
(layout / "index.json").write_bytes(index_bytes)
(blob_dir / config_digest).write_bytes(config_bytes)
(blob_dir / manifest_digest).write_bytes(manifest_bytes)
(blob_dir / layer_digest).write_bytes(layer_bytes)
PY
