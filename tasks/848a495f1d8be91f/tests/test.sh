#!/bin/bash
set -u

mkdir -p /logs/verifier

python3 - <<'PY'
import gzip
import hashlib
import io
import json
import shutil
import stat
import sys
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

def fail(message):
    print(f"FAIL: {message}")
    sys.exit(1)

def read_exact(path):
    try:
        return path.read_bytes()
    except FileNotFoundError:
        fail(f"missing required file: {path}")

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

def build_expected():
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
    return {
        "layout": json_bytes({"imageLayoutVersion": "1.0.0"}),
        "index": json_bytes(index),
        "manifest_digest": manifest_digest,
        "manifest": manifest_bytes,
        "config_digest": config_digest,
        "config": config_bytes,
        "layer_digest": layer_digest,
        "layer": layer_bytes,
        "tar": tar_bytes,
    }

expected = build_expected()

if read_exact(oci / "oci-layout") != expected["layout"]:
    fail("oci-layout is not the required compact OCI layout marker")
if read_exact(oci / "index.json") != expected["index"]:
    fail("index.json content, descriptor digest, size, platform, annotation, ordering, or trailing newline is incorrect")

expected_files = {
    expected["manifest_digest"],
    expected["config_digest"],
    expected["layer_digest"],
}
if not blobdir.is_dir():
    fail("missing blobs/sha256 directory")
actual_files = {p.name for p in blobdir.iterdir() if p.is_file()}
if actual_files != expected_files:
    fail(f"blobs/sha256 has wrong digest file set: {sorted(actual_files)}")

if read_exact(blobdir / expected["manifest_digest"]) != expected["manifest"]:
    fail("manifest blob bytes do not match required OCI manifest")
if read_exact(blobdir / expected["config_digest"]) != expected["config"]:
    fail("config blob bytes do not match required OCI config")
if read_exact(blobdir / expected["layer_digest"]) != expected["layer"]:
    fail("compressed layer bytes are not the required normalized gzip tar")

top_entries = sorted(str(p.relative_to(oci)) for p in oci.rglob("*") if p.is_file())
expected_top = sorted([
    "oci-layout",
    "index.json",
    f"blobs/sha256/{expected['manifest_digest']}",
    f"blobs/sha256/{expected['config_digest']}",
    f"blobs/sha256/{expected['layer_digest']}",
])
if top_entries != expected_top:
    fail(f"OCI layout contains unexpected files: {top_entries}")

try:
    tar_bytes = gzip.decompress(expected["layer"])
except OSError:
    fail("expected layer could not be decompressed")
if tar_bytes != expected["tar"]:
    fail("internal verifier error: expected layer diff_id mismatch")

with gzip.open(blobdir / expected["layer_digest"], "rb") as fh:
    with tarfile.open(fileobj=fh, mode="r:") as tf:
        names = tf.getnames()
        expected_names = [entry[1] for entry in entries]
        if names != expected_names:
            fail(f"layer tar entries are missing, extra, or in the wrong order: {names}")
        for kind, name, mode, payload in entries:
            info = tf.getmember(name)
            if info.uid != 0 or info.gid != 0 or info.uname != "root" or info.gname != "root":
                fail(f"{name} is not owned by root/root in the layer")
            if info.mtime != fixed_mtime:
                fail(f"{name} has non-normalized mtime")
            if stat.S_IMODE(info.mode) != mode:
                fail(f"{name} mode is {oct(stat.S_IMODE(info.mode))}, expected {oct(mode)}")
            if kind == "symlink" and (not info.issym() or info.linkname != payload):
                fail(f"{name} is not the required symlink")
            if kind == "file" and tf.extractfile(info).read() != payload.read_bytes():
                fail(f"{name} content differs from source")

print("ok")
PY

if [ "$?" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
