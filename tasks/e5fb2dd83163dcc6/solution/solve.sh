#!/bin/bash
set -euo pipefail

lab=/home/user/conda_lab
src="$lab/src"
channel="$lab/channel"
noarch="$channel/noarch"
pkg_name=acme-tokens-0.4.0-py_0.tar.bz2

rm -rf "$noarch"
mkdir -p "$noarch"

python3 - <<'PY'
import hashlib
import io
import json
import tarfile
from pathlib import Path

lab = Path("/home/user/conda_lab")
src = lab / "src"
channel = lab / "channel"
noarch = channel / "noarch"
pkg_name = "acme-tokens-0.4.0-py_0.tar.bz2"
pkg_path = noarch / pkg_name
mtime = 1782345600

script = (
    "#!/usr/bin/env python3\n"
    "from acme_tokens.cli import main\n"
    "if __name__ == \"__main__\":\n"
    "    main()\n"
).encode()

runtime = [
    ("site-packages/acme_tokens/__init__.py", (src / "acme_tokens/__init__.py").read_bytes(), 0o644),
    ("site-packages/acme_tokens/cli.py", (src / "acme_tokens/cli.py").read_bytes(), 0o644),
    ("python-scripts/acme-tokens", script, 0o755),
]

index = {
    "arch": None,
    "build": "py_0",
    "build_number": 0,
    "depends": ["python >=3.10"],
    "license": "MIT",
    "name": "acme-tokens",
    "noarch": "python",
    "platform": None,
    "subdir": "noarch",
    "timestamp": 1782345600000,
    "version": "0.4.0",
}
index_bytes = (json.dumps(index, separators=(",", ":")) + "\n").encode()

files_bytes = (
    "site-packages/acme_tokens/__init__.py\n"
    "site-packages/acme_tokens/cli.py\n"
    "python-scripts/acme-tokens\n"
).encode()

paths = {
    "paths": [
        {
            "_path": path,
            "path_type": "hardlink",
            "sha256": hashlib.sha256(data).hexdigest(),
            "size_in_bytes": len(data),
        }
        for path, data, _mode in runtime
    ],
    "paths_version": 1,
}
paths_bytes = (json.dumps(paths, separators=(",", ":")) + "\n").encode()

members = [
    ("info/index.json", index_bytes, 0o644),
    ("info/files", files_bytes, 0o644),
    ("info/paths.json", paths_bytes, 0o644),
] + runtime

def add_bytes(tf, name, data, mode):
    info = tarfile.TarInfo(name)
    info.size = len(data)
    info.mtime = mtime
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mode = mode
    tf.addfile(info, io.BytesIO(data))

with tarfile.open(pkg_path, "w:bz2") as tf:
    for name, data, mode in members:
        add_bytes(tf, name, data, mode)

pkg_bytes = pkg_path.read_bytes()
record = {
    "build": "py_0",
    "build_number": 0,
    "depends": ["python >=3.10"],
    "license": "MIT",
    "md5": hashlib.md5(pkg_bytes).hexdigest(),
    "name": "acme-tokens",
    "noarch": "python",
    "sha256": hashlib.sha256(pkg_bytes).hexdigest(),
    "size": len(pkg_bytes),
    "subdir": "noarch",
    "timestamp": 1782345600000,
    "version": "0.4.0",
}
repodata = {
    "info": {"subdir": "noarch"},
    "packages": {pkg_name: record},
    "packages.conda": {},
    "removed": [],
    "repodata_version": 1,
}
repodata_bytes = json.dumps(repodata, separators=(",", ":")) + "\n"
(noarch / "repodata.json").write_text(repodata_bytes)
(noarch / "current_repodata.json").write_text(repodata_bytes)

channeldata = {
    "channeldata_version": 1,
    "packages": {
        "acme-tokens": {
            "description": "Offline token normalizer",
            "dev_url": "",
            "doc_url": "",
            "home": "https://example.invalid/acme-tokens",
            "license": "MIT",
            "summary": "Offline token normalizer",
            "version": "0.4.0",
        }
    },
    "subdirs": ["noarch"],
}
(channel / "channeldata.json").write_text(json.dumps(channeldata, separators=(",", ":")) + "\n")
PY
