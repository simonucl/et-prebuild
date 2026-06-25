#!/bin/bash
set -u

mkdir -p /logs/verifier
reward=0

if python3 - <<'PY'
import hashlib
import json
import os
import stat
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

lab = Path("/home/user/conda_lab")
src = lab / "src"
channel = lab / "channel"
noarch = channel / "noarch"
pkg_name = "acme-tokens-0.4.0-py_0.tar.bz2"
pkg_path = noarch / pkg_name
repodata_path = noarch / "repodata.json"
current_path = noarch / "current_repodata.json"
channeldata_path = channel / "channeldata.json"

def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)

def expect_file(path, expected):
    if not path.is_file():
        fail(f"missing source file {path}")
    if path.read_bytes() != expected:
        fail(f"source file was modified: {path}")

expect_file(src / "acme_tokens/__init__.py", b'__version__ = "0.4.0"\n')
expect_file(src / "acme_tokens/cli.py", (
    b"import re\n"
    b"import sys\n"
    b"from collections import Counter\n"
    b"\n"
    b"TOKEN_RE = re.compile(r\"[A-Za-z][A-Za-z0-9_-]*\")\n"
    b"\n"
    b"def normalize(text):\n"
    b"    return [match.group(0).upper().replace(\"-\", \"_\") for match in TOKEN_RE.finditer(text)]\n"
    b"\n"
    b"def main(argv=None):\n"
    b"    argv = sys.argv[1:] if argv is None else argv\n"
    b"    text = \" \".join(argv) if argv else sys.stdin.read()\n"
    b"    counts = Counter(normalize(text))\n"
    b"    for token in sorted(counts):\n"
    b"        print(f\"{token}={counts[token]}\")\n"
    b"\n"
    b"if __name__ == \"__main__\":\n"
    b"    main()\n"
))
expect_file(src / "README.md", b"# acme-tokens\n\nSmall offline tokenizer used by release smoke tests.\n")
expect_file(src / "LICENSE", b"MIT License\n\nCopyright 2026 Acme\n")
expect_file(src / "tests/test_cli.py", (
    b"from acme_tokens.cli import normalize\n"
    b"\n"
    b"def test_normalize():\n"
    b"    assert normalize(\"edge-cache beta\") == [\"EDGE_CACHE\", \"BETA\"]\n"
))
expect_file(src / "debug.tmp", b"scratch build note\n")

if not noarch.is_dir():
    fail("channel/noarch directory is missing")
actual_noarch = sorted(p.name for p in noarch.iterdir())
expected_noarch = ["acme-tokens-0.4.0-py_0.tar.bz2", "current_repodata.json", "repodata.json"]
if actual_noarch != expected_noarch:
    fail(f"channel/noarch contains unexpected entries: {actual_noarch}")

channel_entries = sorted(p.name for p in channel.iterdir())
if channel_entries != ["channeldata.json", "noarch"]:
    fail(f"channel root contains unexpected entries: {channel_entries}")

for path in (pkg_path, repodata_path, current_path, channeldata_path):
    if not path.is_file():
        fail(f"missing required file {path}")

expected_names = [
    "info/index.json",
    "info/files",
    "info/paths.json",
    "site-packages/acme_tokens/__init__.py",
    "site-packages/acme_tokens/cli.py",
    "python-scripts/acme-tokens",
]

try:
    with tarfile.open(pkg_path, "r:bz2") as tf:
        infos = tf.getmembers()
        names = [info.name for info in infos]
        if names != expected_names:
            fail(f"unexpected package members or order: {names}")
        contents = {}
        for info in infos:
            if info.isdir():
                fail(f"package must not contain directory entry {info.name}")
            if info.mtime != 1782345600:
                fail(f"{info.name} has non-normalized mtime {info.mtime}")
            if info.uid != 0 or info.gid != 0:
                fail(f"{info.name} has non-normalized uid/gid")
            if info.uname != "" or info.gname != "":
                fail(f"{info.name} has non-empty uname/gname")
            mode = stat.S_IMODE(info.mode)
            expected_mode = 0o755 if info.name == "python-scripts/acme-tokens" else 0o644
            if mode != expected_mode:
                fail(f"{info.name} has mode {oct(mode)}, expected {oct(expected_mode)}")
            extracted = tf.extractfile(info)
            if extracted is None:
                fail(f"could not read {info.name}")
            contents[info.name] = extracted.read()
except (tarfile.TarError, OSError) as exc:
    fail(f"package is not a valid tar.bz2 archive: {exc}")

if contents["site-packages/acme_tokens/__init__.py"] != (src / "acme_tokens/__init__.py").read_bytes():
    fail("__init__.py in package does not match source")
if contents["site-packages/acme_tokens/cli.py"] != (src / "acme_tokens/cli.py").read_bytes():
    fail("cli.py in package does not match source")

expected_script = (
    "#!/usr/bin/env python3\n"
    "from acme_tokens.cli import main\n"
    "if __name__ == \"__main__\":\n"
    "    main()\n"
).encode()
if contents["python-scripts/acme-tokens"] != expected_script:
    fail("python-scripts/acme-tokens content is incorrect")

expected_index = {
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
expected_index_raw = (json.dumps(expected_index, separators=(",", ":")) + "\n").encode()
if contents["info/index.json"] != expected_index_raw:
    fail("info/index.json content, key order, minification, or newline is incorrect")

expected_files = (
    "site-packages/acme_tokens/__init__.py\n"
    "site-packages/acme_tokens/cli.py\n"
    "python-scripts/acme-tokens\n"
).encode()
if contents["info/files"] != expected_files:
    fail("info/files content is incorrect")

runtime_paths = [
    "site-packages/acme_tokens/__init__.py",
    "site-packages/acme_tokens/cli.py",
    "python-scripts/acme-tokens",
]
expected_paths = {
    "paths": [
        {
            "_path": path,
            "path_type": "hardlink",
            "sha256": hashlib.sha256(contents[path]).hexdigest(),
            "size_in_bytes": len(contents[path]),
        }
        for path in runtime_paths
    ],
    "paths_version": 1,
}
expected_paths_raw = (json.dumps(expected_paths, separators=(",", ":")) + "\n").encode()
if contents["info/paths.json"] != expected_paths_raw:
    fail("info/paths.json content, hashes, sizes, key order, or newline is incorrect")

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
expected_repodata = {
    "info": {"subdir": "noarch"},
    "packages": {pkg_name: record},
    "packages.conda": {},
    "removed": [],
    "repodata_version": 1,
}
expected_repodata_raw = json.dumps(expected_repodata, separators=(",", ":")) + "\n"
if repodata_path.read_text() != expected_repodata_raw:
    fail("repodata.json content, digests, key order, minification, or newline is incorrect")
if current_path.read_text() != expected_repodata_raw:
    fail("current_repodata.json must match the expected package record exactly")

expected_channeldata = {
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
expected_channeldata_raw = json.dumps(expected_channeldata, separators=(",", ":")) + "\n"
if channeldata_path.read_text() != expected_channeldata_raw:
    fail("channeldata.json content, key order, minification, or newline is incorrect")

with tempfile.TemporaryDirectory() as td:
    prefix = Path(td) / "prefix"
    prefix.mkdir()
    with tarfile.open(pkg_path, "r:bz2") as tf:
        tf.extractall(prefix)
    script = prefix / "python-scripts/acme-tokens"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(prefix / "site-packages")
    run = subprocess.run(
        [sys.executable, str(script), " Edge-cache edge cache beta beta "],
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if run.returncode != 0:
        fail(f"installed script failed: {run.stderr}")
    if run.stdout != "BETA=2\nCACHE=1\nEDGE=1\nEDGE_CACHE=1\n":
        fail(f"installed script output is wrong: {run.stdout!r}")

print("conda noarch channel validated")
PY
then
  reward=1
fi

echo "$reward" > /logs/verifier/reward.txt
