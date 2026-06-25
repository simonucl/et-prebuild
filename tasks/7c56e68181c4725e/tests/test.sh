#!/bin/bash
set -u

mkdir -p /logs/verifier
reward=0
ROOT="${ROOT_PREFIX:-}"

if python3 - "$ROOT" <<'PY'
import gzip
import hashlib
import io
import json
import os
import stat
import sys
import tarfile
from pathlib import Path

root = Path(sys.argv[1]) if sys.argv[1] else Path("/")
stage = root / "home/user/oci-stage"
rootfs = stage / "rootfs"
out = root / "home/user/oci-export/acme-cache_1.2.0"
blob_dir = out / "blobs/sha256"

expected_layer_names = [
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

expected_stage_text = {
    "etc/acme-cache/config.yaml": "listen: 127.0.0.1:9184\nmode: strict\ncache_ttl: 3600\n",
    "usr/local/bin/acme-cache": '#!/usr/bin/env bash\nset -euo pipefail\nprintf "acme-cache 1.2.0\\n"\n',
    "var/lib/acme-cache/seed.txt": "seed=offline\nwindow=2024q4\n",
}

def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)

def read_json_exact(path: Path):
    data = path.read_bytes()
    if not data.endswith(b"\n") or data.count(b"\n") != 1:
        fail(f"{path.name} must be minified JSON with exactly one trailing newline")
    try:
        return data, json.loads(data)
    except json.JSONDecodeError as exc:
        fail(f"{path.name} is not valid JSON: {exc}")

if not out.is_dir():
    fail("missing OCI layout output directory")
if not blob_dir.is_dir():
    fail("missing blobs/sha256 directory")

top_entries = sorted(p.name for p in out.iterdir())
if top_entries != ["blobs", "index.json", "oci-layout"]:
    fail(f"top-level OCI layout contains unexpected entries: {top_entries}")
if sorted(p.name for p in (out / "blobs").iterdir()) != ["sha256"]:
    fail("blobs directory must contain only sha256")

for rel, text in expected_stage_text.items():
    path = rootfs / rel
    if not path.is_file() or path.read_text(encoding="utf-8") != text:
        fail(f"staged source file was modified: {rel}")
if not (rootfs / "etc/acme-cache/current").is_symlink() or os.readlink(rootfs / "etc/acme-cache/current") != "config.yaml":
    fail("staged symlink was modified")
if not (rootfs / "tmp/session.tmp").is_file() or not (rootfs / "tests/fixture.txt").is_file():
    fail("staged source-only files were deleted")
if not (stage / "notes/operator.md").is_file():
    fail("staged notes were deleted")

layout_bytes = (out / "oci-layout").read_bytes() if (out / "oci-layout").is_file() else b""
if layout_bytes != b'{"imageLayoutVersion":"1.0.0"}\n':
    fail("oci-layout content is incorrect")

index_bytes, index = read_json_exact(out / "index.json")
if list(index.keys()) != ["schemaVersion", "manifests"]:
    fail("index.json has wrong top-level key order")
if index["schemaVersion"] != 2 or not isinstance(index["manifests"], list) or len(index["manifests"]) != 1:
    fail("index.json schemaVersion or manifests array is incorrect")
manifest_desc = index["manifests"][0]
if list(manifest_desc.keys()) != ["mediaType", "digest", "size", "annotations"]:
    fail("manifest descriptor has wrong key order")
if manifest_desc.get("mediaType") != "application/vnd.oci.image.manifest.v1+json":
    fail("index uses wrong manifest mediaType")
if manifest_desc.get("annotations") != {"org.opencontainers.image.ref.name": "acme-cache:1.2.0"}:
    fail("index annotations are incorrect")

blob_names = sorted(p.name for p in blob_dir.iterdir() if p.is_file())
if len(blob_names) != 3 or any(len(name) != 64 or not all(c in "0123456789abcdef" for c in name) for name in blob_names):
    fail(f"blobs/sha256 must contain exactly three lowercase sha256 blob files, found {blob_names}")

def descriptor_blob(desc, label: str) -> bytes:
    digest = desc.get("digest", "")
    if not digest.startswith("sha256:"):
        fail(f"{label} descriptor digest must use sha256")
    name = digest.split(":", 1)[1]
    path = blob_dir / name
    if not path.is_file():
        fail(f"{label} blob file is missing")
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != name:
        fail(f"{label} blob filename does not match its sha256 digest")
    if desc.get("size") != len(data):
        fail(f"{label} descriptor size does not match blob length")
    return data

manifest_blob = descriptor_blob(manifest_desc, "manifest")
manifest = json.loads(manifest_blob)
if not manifest_blob.endswith(b"\n") or manifest_blob.count(b"\n") != 1:
    fail("manifest blob must be minified JSON with exactly one trailing newline")
if list(manifest.keys()) != ["schemaVersion", "mediaType", "config", "layers", "annotations"]:
    fail("manifest top-level keys are in the wrong order")
if manifest["schemaVersion"] != 2:
    fail("manifest schemaVersion is incorrect")
if manifest["mediaType"] != "application/vnd.oci.image.manifest.v1+json":
    fail("manifest mediaType is incorrect")
if manifest["annotations"] != {"org.opencontainers.image.version": "1.2.0"}:
    fail("manifest annotations are incorrect")
if list(manifest["config"].keys()) != ["mediaType", "digest", "size"]:
    fail("config descriptor keys are in the wrong order")
if manifest["config"]["mediaType"] != "application/vnd.oci.image.config.v1+json":
    fail("config mediaType is incorrect")
if not isinstance(manifest["layers"], list) or len(manifest["layers"]) != 1:
    fail("manifest must contain exactly one layer")
layer_desc = manifest["layers"][0]
if list(layer_desc.keys()) != ["mediaType", "digest", "size"]:
    fail("layer descriptor keys are in the wrong order")
if layer_desc["mediaType"] != "application/vnd.oci.image.layer.v1.tar+gzip":
    fail("layer mediaType is incorrect")

config_blob = descriptor_blob(manifest["config"], "config")
if not config_blob.endswith(b"\n") or config_blob.count(b"\n") != 1:
    fail("config blob must be minified JSON with exactly one trailing newline")
config = json.loads(config_blob)
if list(config.keys()) != ["created", "architecture", "os", "config", "rootfs", "history"]:
    fail("config top-level keys are in the wrong order")
if config.get("created") != "2024-02-03T04:05:06Z" or config.get("architecture") != "amd64" or config.get("os") != "linux":
    fail("config metadata does not match staged image-meta.json")
if config.get("config") != {"Env": ["PATH=/usr/local/bin:/usr/bin:/bin"], "Cmd": ["/usr/local/bin/acme-cache"]}:
    fail("config process settings are incorrect")
if config.get("history") != [{"created": "2024-02-03T04:05:06Z", "created_by": "manual offline rootfs import"}]:
    fail("config history is incorrect")

layer_blob = descriptor_blob(layer_desc, "layer")
if len(layer_blob) < 18 or layer_blob[:2] != b"\x1f\x8b" or layer_blob[2] != 8:
    fail("layer blob is not a gzip stream")
flags = layer_blob[3]
mtime = int.from_bytes(layer_blob[4:8], "little")
if mtime != 0:
    fail("gzip mtime must be zero")
if flags & 0x08:
    fail("gzip stream must not store an original filename")

try:
    layer_plain = gzip.decompress(layer_blob)
except OSError as exc:
    fail(f"layer gzip stream cannot be decompressed: {exc}")
diff_id = hashlib.sha256(layer_plain).hexdigest()
if config.get("rootfs") != {"type": "layers", "diff_ids": [f"sha256:{diff_id}"]}:
    fail("rootfs diff_id does not match uncompressed layer tar")

with tarfile.open(fileobj=io.BytesIO(layer_plain), mode="r:") as tf:
    members = tf.getmembers()
    names = [member.name for member in members]
    if names != expected_layer_names:
        fail(f"unexpected layer tar members or order: {names!r}")
    by_name = {member.name: member for member in members}
    for member in members:
        if member.uid != 0 or member.gid != 0 or member.uname or member.gname:
            fail(f"{member.name} does not use numeric 0/0 ownership")
        if member.mtime != 1704067200:
            fail(f"{member.name} has non-normalized mtime")
    for name in ["etc", "etc/acme-cache", "usr", "usr/local", "usr/local/bin", "var", "var/lib", "var/lib/acme-cache"]:
        member = by_name[name]
        if not member.isdir() or stat.S_IMODE(member.mode) != 0o755:
            fail(f"{name} is not a 0755 directory")
    for name in ["etc/acme-cache/config.yaml", "var/lib/acme-cache/seed.txt"]:
        member = by_name[name]
        if not member.isfile() or stat.S_IMODE(member.mode) != 0o644:
            fail(f"{name} is not a 0644 regular file")
        extracted = tf.extractfile(member)
        if extracted is None or extracted.read() != (rootfs / name).read_bytes():
            fail(f"{name} content does not match the staged source")
    script = by_name["usr/local/bin/acme-cache"]
    if not script.isfile() or stat.S_IMODE(script.mode) != 0o755:
        fail("usr/local/bin/acme-cache is not a 0755 regular file")
    extracted_script = tf.extractfile(script)
    if extracted_script is None or extracted_script.read() != (rootfs / "usr/local/bin/acme-cache").read_bytes():
        fail("usr/local/bin/acme-cache content does not match the staged source")
    link = by_name["etc/acme-cache/current"]
    if not link.issym() or link.linkname != "config.yaml":
        fail("etc/acme-cache/current is not the required symlink")

for forbidden in ["tmp", "tests", "operator.md", "session.tmp", "fixture.txt"]:
    if forbidden in index_bytes.decode("utf-8", errors="ignore") or any(forbidden in name for name in blob_names):
        fail(f"layout metadata mentions forbidden source-only artifact {forbidden}")
    if forbidden.encode() in layer_plain:
        fail(f"layer contains forbidden source-only artifact {forbidden}")

print("all checks passed")
PY
then
  reward=1
fi

echo "$reward" > /logs/verifier/reward.txt
exit 0
