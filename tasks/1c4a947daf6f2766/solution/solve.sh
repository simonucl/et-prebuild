#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import base64
import gzip
import hashlib
import io
import json
import os
import tarfile
from collections import OrderedDict
from pathlib import Path

root = Path(os.environ.get("TRSI_ROOT", "/"))
def ap(path):
    return root / path.lstrip("/")

src = ap("/home/user/npm-lab/src/edge-policy")
repo = ap("/home/user/npm-lab/registry/@acme/edge-policy")
tar_rel = Path("-/edge-policy-1.3.0.tgz")
tar_path = repo / tar_rel

for child in list(repo.iterdir()):
    if child.is_dir():
        for root, dirs, files in os.walk(child, topdown=False):
            for name in files:
                Path(root, name).unlink()
            for name in dirs:
                Path(root, name).rmdir()
        child.rmdir()
    else:
        child.unlink()

(repo / "-").mkdir(parents=True, exist_ok=True)

package_json = OrderedDict([
    ("name", "@acme/edge-policy"),
    ("version", "1.3.0"),
    ("description", "Offline edge policy compiler"),
    ("type", "module"),
    ("main", "dist/index.js"),
    ("types", "types/index.d.ts"),
    ("bin", OrderedDict([("edge-policy", "bin/edge-policy.js")])),
    ("files", ["dist", "bin", "types", "README.md", "LICENSE"]),
    ("license", "MIT"),
    ("engines", OrderedDict([("node", ">=20")])),
])

members = [
    ("package/package.json", json.dumps(package_json, separators=(",", ":")).encode() + b"\n", 0o644),
    ("package/README.md", (src / "README.md").read_bytes(), 0o644),
    ("package/LICENSE", (src / "LICENSE").read_bytes(), 0o644),
    ("package/dist/index.js", (src / "dist/index.js").read_bytes(), 0o644),
    ("package/dist/rules.json", (src / "dist/rules.json").read_bytes(), 0o644),
    ("package/bin/edge-policy.js", (src / "bin/edge-policy.js").read_bytes(), 0o755),
    ("package/types/index.d.ts", (src / "types/index.d.ts").read_bytes(), 0o644),
]

raw_tar = io.BytesIO()
with tarfile.open(fileobj=raw_tar, mode="w", format=tarfile.USTAR_FORMAT) as tf:
    for name, data, mode in members:
        ti = tarfile.TarInfo(name)
        ti.size = len(data)
        ti.mtime = 1782345600
        ti.uid = 0
        ti.gid = 0
        ti.uname = ""
        ti.gname = ""
        ti.mode = mode
        tf.addfile(ti, io.BytesIO(data))

with tar_path.open("wb") as f:
    with gzip.GzipFile(filename="", mode="wb", fileobj=f, compresslevel=9, mtime=0) as gz:
        gz.write(raw_tar.getvalue())

tar_bytes = tar_path.read_bytes()
sha1 = hashlib.sha1(tar_bytes).hexdigest()
integrity = "sha512-" + base64.b64encode(hashlib.sha512(tar_bytes).digest()).decode()
unpacked = sum(len(data) for _, data, _ in members)

version_obj = OrderedDict([
    ("name", "@acme/edge-policy"),
    ("version", "1.3.0"),
    ("description", "Offline edge policy compiler"),
    ("license", "MIT"),
    ("main", "dist/index.js"),
    ("types", "types/index.d.ts"),
    ("bin", OrderedDict([("edge-policy", "bin/edge-policy.js")])),
    ("dist", OrderedDict([
        ("tarball", "/@acme/edge-policy/-/edge-policy-1.3.0.tgz"),
        ("shasum", sha1),
        ("integrity", integrity),
        ("unpackedSize", unpacked),
    ])),
])
packument = OrderedDict([
    ("_id", "@acme/edge-policy"),
    ("name", "@acme/edge-policy"),
    ("dist-tags", OrderedDict([("latest", "1.3.0")])),
    ("versions", OrderedDict([("1.3.0", version_obj)])),
    ("time", OrderedDict([
        ("created", "2026-06-25T00:00:00.000Z"),
        ("modified", "2026-06-25T00:00:00.000Z"),
        ("1.3.0", "2026-06-25T00:00:00.000Z"),
    ])),
])
(repo / "index.json").write_text(json.dumps(packument, separators=(",", ":")) + "\n")

files = []
for name, data, _ in members:
    files.append(OrderedDict([
        ("path", name),
        ("sha256", hashlib.sha256(data).hexdigest()),
        ("size_bytes", len(data)),
    ]))
manifest = OrderedDict([
    ("package", "@acme/edge-policy"),
    ("version", "1.3.0"),
    ("tarball", "-/edge-policy-1.3.0.tgz"),
    ("sha1", sha1),
    ("integrity", integrity),
    ("size_bytes", len(tar_bytes)),
    ("files", files),
])
(repo / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n")
PY
