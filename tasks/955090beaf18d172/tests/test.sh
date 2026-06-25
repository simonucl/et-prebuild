#!/bin/bash
set -u

mkdir -p /logs/verifier

if python3 - <<'PY'
import gzip
import hashlib
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path("/home/user/oci-dual")
basefs = root / "basefs"
patchfs = root / "patchfs"
image = root / "image"
blobdir = image / "blobs" / "sha256"
created = "2025-02-14T12:00:00Z"
mtime = "@1739534400"

expected_base = {
    "etc/netprobe/defaults.yaml": (b"listen: 127.0.0.1:9000\nmode: lab\nsample_rate: 10\n", 0o644),
    "usr/local/bin/netprobe": (b'#!/bin/sh\nset -eu\nprintf "netprobe base\\n"\n', 0o755),
    "usr/share/netprobe/schema.json": (b'{"type":"object","required":["listen","mode","sample_rate"]}\n', 0o644),
    "var/lib/netprobe/cache/state.txt": (b"checkpoint=17\n", 0o644),
}
expected_patch = {
    "etc/netprobe/config.yaml": (b"listen: 0.0.0.0:9443\nmode: offline\nsample_rate: 3\nsink: file\n", 0o640),
    "usr/local/bin/netprobe": (b'#!/bin/sh\nset -eu\nprintf "netprobe offline 2.1.0\\n"\n', 0o755),
    "var/lib/netprobe/cache/state.txt": (b"checkpoint=0\n", 0o644),
}

def fail(message: str) -> None:
    print("FAIL:", message, file=sys.stderr)
    raise SystemExit(1)

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def descriptor(data: bytes) -> tuple[str, int]:
    return "sha256:" + sha256(data), len(data)

def minjson(obj) -> bytes:
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False).encode() + b"\n"

def require_tree(path: Path, expected: dict[str, tuple[bytes, int]], name: str) -> None:
    actual = sorted(str(p.relative_to(path)) for p in path.rglob("*") if p.is_file())
    if actual != sorted(expected):
        fail(f"{name} file set was modified: {actual}")
    for rel, (data, mode) in expected.items():
        p = path / rel
        if p.read_bytes() != data:
            fail(f"{name} content was modified: {rel}")
        if stat.S_IMODE(p.stat().st_mode) != mode:
            fail(f"{name} mode for {rel} is {stat.S_IMODE(p.stat().st_mode):04o}, expected {mode:04o}")

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

def read_exact_json(path: Path, expected_obj, label: str) -> None:
    data = path.read_bytes()
    if data != minjson(expected_obj):
        fail(f"{label} content, key order, minification, or newline is incorrect")
    try:
        parsed = json.loads(data)
    except json.JSONDecodeError as exc:
        fail(f"{label} is not valid JSON: {exc}")
    if parsed != expected_obj:
        fail(f"{label} JSON values are incorrect")

require_tree(basefs, expected_base, "basefs")
require_tree(patchfs, expected_patch, "patchfs")

if (image / "oci-layout").read_bytes() != b'{"imageLayoutVersion":"1.0.0"}\n':
    fail("oci-layout content is incorrect")
if not blobdir.is_dir():
    fail("missing image/blobs/sha256 directory")

blob_files = sorted(p for p in blobdir.iterdir() if p.is_file())
if len(blob_files) != 4:
    fail("image/blobs/sha256 must contain exactly four blob files")
for p in blob_files:
    data = p.read_bytes()
    if p.name != sha256(data):
        fail(f"blob filename does not match sha256 digest: {p.name}")

base_tar = tar_tree(basefs)
base_layer = gz(base_tar)
base_digest, base_size = descriptor(base_layer)
base_diff = "sha256:" + sha256(base_tar)
base_path = blobdir / base_digest.split(":", 1)[1]
if not base_path.is_file() or base_path.read_bytes() != base_layer:
    fail("base layer blob is not the required deterministic gzip tar")

with tempfile.TemporaryDirectory() as td:
    update_root = Path(td) / "update"
    shutil.copytree(patchfs, update_root, symlinks=True)
    whiteout = update_root / "etc/netprobe/.wh.defaults.yaml"
    whiteout.write_bytes(b"")
    os.chmod(whiteout, 0o600)
    update_tar = tar_tree(update_root)

update_layer = gz(update_tar)
update_digest, update_size = descriptor(update_layer)
update_diff = "sha256:" + sha256(update_tar)
update_path = blobdir / update_digest.split(":", 1)[1]
if not update_path.is_file() or update_path.read_bytes() != update_layer:
    fail("update layer blob is not the required deterministic gzip tar with whiteout")

for label, data in [("base layer", base_layer), ("update layer", update_layer)]:
    if data[3] & 0x08:
        fail(f"{label} gzip stores an original filename")
    if int.from_bytes(data[4:8], "little") != 0:
        fail(f"{label} gzip mtime is not zero")
    gzip.decompress(data)

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
config_digest, config_size = descriptor(config_bytes)
config_path = blobdir / config_digest.split(":", 1)[1]
if not config_path.is_file():
    fail("missing config blob with expected digest")
read_exact_json(config_path, config, "config blob")

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
manifest_digest, manifest_size = descriptor(manifest_bytes)
manifest_path = blobdir / manifest_digest.split(":", 1)[1]
if not manifest_path.is_file():
    fail("missing manifest blob with expected digest")
read_exact_json(manifest_path, manifest, "manifest blob")

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
read_exact_json(image / "index.json", index, "index.json")
PY
then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
