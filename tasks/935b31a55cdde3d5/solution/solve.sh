#!/bin/bash
set -euo pipefail

pkg=/home/user/npm-lab/widget-kit
handoff=/home/user/npm-lab/handoff
tarball=acme-widget-kit-1.6.4.tgz

rm -rf "$handoff"
mkdir -p "$handoff"

cd "$pkg"
npm pack --pack-destination "$handoff" >/tmp/widget-kit-npm-pack.json

cd "$handoff"
sha256sum "$tarball" > SHA256SUMS

python3 - <<'PY'
import base64
import hashlib
import json
import tarfile
from pathlib import Path

handoff = Path("/home/user/npm-lab/handoff")
tarball = handoff / "acme-widget-kit-1.6.4.tgz"
blob = tarball.read_bytes()

files = []
with tarfile.open(tarball, "r:gz") as tf:
    for member in tf.getmembers():
        extracted = tf.extractfile(member)
        data = extracted.read() if extracted is not None else b""
        files.append({
            "path": member.name,
            "mode": format(member.mode & 0o7777, "04o"),
            "size": member.size,
            "sha256": hashlib.sha256(data).hexdigest(),
        })

manifest = {
    "package": "@acme/widget-kit",
    "version": "1.6.4",
    "tarball": "acme-widget-kit-1.6.4.tgz",
    "sha256": hashlib.sha256(blob).hexdigest(),
    "sha1": hashlib.sha1(blob).hexdigest(),
    "integrity": "sha512-" + base64.b64encode(hashlib.sha512(blob).digest()).decode("ascii"),
    "entry_count": len(files),
    "files": files,
}
(handoff / "package-manifest.json").write_text(
    json.dumps(manifest, separators=(",", ":")) + "\n",
    encoding="utf-8",
)
PY
