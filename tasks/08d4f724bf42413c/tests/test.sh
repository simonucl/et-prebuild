#!/bin/bash
set -u

mkdir -p /logs/verifier
reward=0
tmp="$(mktemp -d)"

cleanup() {
  rm -rf "$tmp"
}
trap cleanup EXIT

fail() {
  echo "FAIL: $*" >&2
  echo "$reward" > /logs/verifier/reward.txt
  exit 1
}

python3 - <<'PY' > "$tmp/expected.json"
import gzip
import hashlib
import io
import json
import stat
import tarfile
from pathlib import Path

root = Path("/app/rootfs")
layout = Path("/app/oci-layout")
created = "2024-06-02T00:00:00Z"
tar_mtime = 1717286400
ref = "registry.example.com/acme/edge-gateway:2.4.1"

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
oci_layout_bytes = b'{"imageLayoutVersion":"1.0.0"}\n'

expected = {
    "digests": {
        "config": config_digest,
        "manifest": manifest_digest,
        "layer": layer_digest,
        "diff": diff_digest,
    },
    "sizes": {
        "config": len(config_bytes),
        "manifest": len(manifest_bytes),
        "layer": len(layer_bytes),
    },
    "files": {
        "oci-layout": oci_layout_bytes.hex(),
        "index.json": index_bytes.hex(),
        f"blobs/sha256/{config_digest}": config_bytes.hex(),
        f"blobs/sha256/{manifest_digest}": manifest_bytes.hex(),
        f"blobs/sha256/{layer_digest}": layer_bytes.hex(),
    },
    "tar_entries": [rel for rel, _ in entries],
}
print(json.dumps(expected, separators=(",", ":")))
PY

[ "$?" -eq 0 ] || fail "could not build verifier reference layout"

python3 - "$tmp/expected.json" <<'PY'
import gzip
import hashlib
import io
import json
import stat
import sys
import tarfile
from pathlib import Path

layout = Path("/app/oci-layout")
expected = json.loads(Path(sys.argv[1]).read_text())

def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)

if not layout.is_dir():
    fail("/app/oci-layout is missing")

actual_files = sorted(
    p.relative_to(layout).as_posix()
    for p in layout.rglob("*")
    if p.is_file()
)
expected_files = sorted(expected["files"])
if actual_files != expected_files:
    fail(f"layout file set is wrong: {actual_files}")

for rel, expected_hex in expected["files"].items():
    path = layout / rel
    data = path.read_bytes()
    if data != bytes.fromhex(expected_hex):
        fail(f"{rel} content does not match the required deterministic OCI layout")

blob_dir = layout / "blobs" / "sha256"
for blob in blob_dir.iterdir():
    if not blob.is_file():
        fail(f"unexpected non-file in blobs/sha256: {blob.name}")
    digest = hashlib.sha256(blob.read_bytes()).hexdigest()
    if digest != blob.name:
        fail(f"blob {blob.name} content digest is sha256:{digest}")

layer_path = blob_dir / expected["digests"]["layer"]
with gzip.GzipFile(fileobj=io.BytesIO(layer_path.read_bytes()), mode="rb") as gz:
    tar_bytes = gz.read()
if hashlib.sha256(tar_bytes).hexdigest() != expected["digests"]["diff"]:
    fail("uncompressed layer digest does not match rootfs.diff_ids")

with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:") as tf:
    infos = tf.getmembers()
    names = [info.name for info in infos]
    if names != expected["tar_entries"]:
        fail(f"layer tar member order or exclusions are wrong: {names}")
    for info in infos:
        if info.uid != 0 or info.gid != 0 or info.uname != "root" or info.gname != "root":
            fail(f"{info.name} does not have normalized root ownership")
        if info.mtime != 1717286400:
            fail(f"{info.name} has mtime {info.mtime}, expected 1717286400")
        mode = stat.S_IMODE(info.mode)
        if info.isdir() and mode != 0o755:
            fail(f"{info.name} directory mode is {oct(mode)}, expected 0o755")
        if info.isfile():
            expected_mode = 0o755 if info.name == "usr/local/bin/edge-gateway" else 0o644
            if mode != expected_mode:
                fail(f"{info.name} mode is {oct(mode)}, expected {oct(expected_mode)}")
        if info.name.startswith("run/") or info.name == "run" or info.name.startswith("tmp/") or info.name == "tmp":
            fail(f"excluded transient path appears in layer: {info.name}")

index = json.loads((layout / "index.json").read_bytes())
manifest_desc = index["manifests"][0]
if manifest_desc["digest"] != f"sha256:{expected['digests']['manifest']}":
    fail("index manifest digest does not point to the manifest blob")
manifest = json.loads((blob_dir / expected["digests"]["manifest"]).read_bytes())
if manifest["config"]["digest"] != f"sha256:{expected['digests']['config']}":
    fail("manifest config digest is wrong")
if manifest["layers"][0]["digest"] != f"sha256:{expected['digests']['layer']}":
    fail("manifest layer digest is wrong")
config = json.loads((blob_dir / expected["digests"]["config"]).read_bytes())
if config["rootfs"]["diff_ids"] != [f"sha256:{expected['digests']['diff']}"]:
    fail("config rootfs.diff_ids is wrong")
PY

if [ "$?" -eq 0 ]; then
  reward=1
  echo "$reward" > /logs/verifier/reward.txt
  echo "ok"
else
  echo "$reward" > /logs/verifier/reward.txt
  exit 1
fi

