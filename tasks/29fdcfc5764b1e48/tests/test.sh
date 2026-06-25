#!/bin/bash
set -u

mkdir -p /logs/verifier
reward=0

fail() {
  echo "FAIL: $*" >&2
  echo "$reward" > /logs/verifier/reward.txt
  exit 1
}

python3 - <<'PY'
import gzip
import hashlib
import io
import json
import os
import stat
import sys
import tarfile
from pathlib import Path

ROOT = Path("/app/rootfs")
OCI = Path("/app/oci")
BLOBS = OCI / "blobs" / "sha256"
CREATED = "2024-01-01T00:00:00Z"
MTIME = 1704067200
REF = "registry.example.test/edgecache:1.2.0"

def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)

def read_exact(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except FileNotFoundError:
        fail(f"missing required file: {path}")

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

def load_json_exact(path: Path):
    raw = read_exact(path)
    if not raw.endswith(b"\n") or raw.count(b"\n") != 1:
        fail(f"{path} must be single-line JSON with one trailing newline")
    try:
        return json.loads(raw), raw
    except json.JSONDecodeError as exc:
        fail(f"{path} is not valid JSON: {exc}")

if read_exact(OCI / "oci-layout") != b'{"imageLayoutVersion":"1.0.0"}\n':
    fail("oci-layout content is incorrect")

raw_layer = tar_bytes()
diff_id = digest(raw_layer)
expected_layer = gzip_bytes(raw_layer)
layer_digest = digest(expected_layer)

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
expected_config = json_bytes(config)
config_digest = digest(expected_config)

manifest = {
    "schemaVersion": 2,
    "mediaType": "application/vnd.oci.image.manifest.v1+json",
    "config": {
        "mediaType": "application/vnd.oci.image.config.v1+json",
        "digest": f"sha256:{config_digest}",
        "size": len(expected_config),
    },
    "layers": [
        {
            "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
            "digest": f"sha256:{layer_digest}",
            "size": len(expected_layer),
        }
    ],
}
expected_manifest = json_bytes(manifest)
manifest_digest = digest(expected_manifest)

index = {
    "schemaVersion": 2,
    "mediaType": "application/vnd.oci.image.index.v1+json",
    "manifests": [
        {
            "mediaType": "application/vnd.oci.image.manifest.v1+json",
            "digest": f"sha256:{manifest_digest}",
            "size": len(expected_manifest),
            "platform": {"architecture": "amd64", "os": "linux"},
            "annotations": {"org.opencontainers.image.ref.name": REF},
        }
    ],
}
expected_index = json_bytes(index)

if read_exact(BLOBS / layer_digest) != expected_layer:
    fail("layer blob is missing or not the required deterministic gzip tar")
if read_exact(BLOBS / config_digest) != expected_config:
    fail("config blob content, ordering, digest, or trailing newline is incorrect")
if read_exact(BLOBS / manifest_digest) != expected_manifest:
    fail("manifest blob content, descriptors, ordering, or trailing newline is incorrect")
if read_exact(OCI / "index.json") != expected_index:
    fail("index.json content, descriptor digest, size, platform, annotation, or formatting is incorrect")

expected_blob_names = {layer_digest, config_digest, manifest_digest}
actual_blob_names = {p.name for p in BLOBS.iterdir() if p.is_file()}
if actual_blob_names != expected_blob_names:
    fail(f"blobs/sha256 has unexpected files: {sorted(actual_blob_names)}")

with gzip.GzipFile(fileobj=io.BytesIO(read_exact(BLOBS / layer_digest)), mode="rb") as gz:
    layer_tar = gz.read()
if digest(layer_tar) != diff_id:
    fail("layer diff_id does not match the config rootfs diff_id")

with tarfile.open(fileobj=io.BytesIO(layer_tar), mode="r:") as tf:
    infos = tf.getmembers()
    names = [info.name for info in infos]
    expected_names = [rel for rel, _ in iter_entries()]
    if names != expected_names:
        fail(f"layer tar entries are missing, extra, or unsorted: {names}")
    for info in infos:
        if info.uid != 0 or info.gid != 0 or info.uname != "root" or info.gname != "root":
            fail(f"{info.name} ownership is not normalized to root/root")
        if info.mtime != MTIME:
            fail(f"{info.name} timestamp is not normalized")
        if info.isdir() and (info.mode & 0o777) != 0o755:
            fail(f"{info.name} directory mode is not 0755")
        if info.isfile():
            expected_mode = 0o755 if info.name == "usr/local/bin/edgecache" else 0o644
            if (info.mode & 0o777) != expected_mode:
                fail(f"{info.name} mode is {oct(info.mode & 0o777)}, expected {oct(expected_mode)}")
        if info.issym() and (info.name != "etc/edgecache/current.toml" or info.linkname != "edgecache.toml"):
            fail("current.toml symlink was not preserved correctly")

if "var/cache/edgecache/index.db" in expected_names or "etc/edgecache/edgecache.toml.tmp" in expected_names:
    fail("verifier internal exclude list is wrong")
PY

if [ "$?" -eq 0 ]; then
  reward=1
  echo "$reward" > /logs/verifier/reward.txt
  echo "ok"
else
  echo "$reward" > /logs/verifier/reward.txt
  exit 1
fi
