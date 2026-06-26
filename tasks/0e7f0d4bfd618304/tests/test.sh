#!/bin/bash
set -euo pipefail

mkdir -p /logs/verifier

python3 - <<'PY'
import base64
import gzip
import hashlib
import io
import json
import os
import sys
import tarfile
from collections import OrderedDict
from pathlib import Path

ROOT = Path("/app/yarn-lab")
PKG = ROOT / "packages"
MIRROR = ROOT / "mirror"
MTIME = 1782345600

def fail(msg):
    print("FAIL:", msg)
    Path("/logs/verifier/reward.txt").write_text("0\n")
    sys.exit(0)

def minjson(obj):
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False).encode() + b"\n"

def read(rel):
    return (PKG / rel).read_bytes()

if not ROOT.exists():
    fail("/app/yarn-lab is missing")

source_expected = {
    "edge-flags/package.json": b'{"name":"@acme/edge-flags","version":"1.1.9","description":"draft metadata","main":"src/index.js"}\n',
    "edge-flags/src/index.js": b'export const FLAGS = Object.freeze({"betaRules":true,"auditSink":"spool"});\n',
    "edge-flags/README.md": b"# Edge Flags\n\nOffline feature flag constants for edge deployments.\n",
    "edge-flags/LICENSE": b"MIT License\n\nCopyright (c) 2026 Acme\n",
    "policy-table/package.json": b'{"name":"@acme/policy-table","version":"0.5.0","description":"old metadata","main":"index.js"}\n',
    "policy-table/index.js": b'import { FLAGS } from "@acme/edge-flags";\nexport function policyTable() {\n  return { flags: FLAGS, defaults: { mode: "enforce", sampleRate: 1 } };\n}\n',
    "policy-table/data/defaults.json": b'{"mode":"enforce","sampleRate":1,"outputs":["json","syslog"]}\n',
}

for rel, expected in source_expected.items():
    path = PKG / rel
    if not path.exists() or path.read_bytes() != expected:
        fail(f"source tree was modified or is missing {rel}")

expected_mirror = ["@acme-edge-flags-1.2.0.tgz", "@acme-policy-table-0.5.1.tgz"]
if not MIRROR.is_dir():
    fail("mirror directory is missing")
actual_mirror = sorted(p.name for p in MIRROR.iterdir() if p.is_file() or p.is_dir())
if actual_mirror != expected_mirror:
    fail(f"mirror contains unexpected entries: {actual_mirror}")

edge_pkg = OrderedDict([
    ("name", "@acme/edge-flags"),
    ("version", "1.2.0"),
    ("description", "Offline edge feature flags"),
    ("type", "module"),
    ("main", "src/index.js"),
    ("files", ["src", "README.md", "LICENSE"]),
    ("license", "MIT"),
])
policy_pkg = OrderedDict([
    ("name", "@acme/policy-table"),
    ("version", "0.5.1"),
    ("description", "Offline policy defaults table"),
    ("type", "module"),
    ("main", "index.js"),
    ("files", ["index.js", "data"]),
    ("dependencies", OrderedDict([("@acme/edge-flags", "1.2.0")])),
    ("license", "Apache-2.0"),
])

specs = {
    "@acme-edge-flags-1.2.0.tgz": [
        ("package/package.json", minjson(edge_pkg)),
        ("package/README.md", source_expected["edge-flags/README.md"]),
        ("package/LICENSE", source_expected["edge-flags/LICENSE"]),
        ("package/src/index.js", source_expected["edge-flags/src/index.js"]),
    ],
    "@acme-policy-table-0.5.1.tgz": [
        ("package/package.json", minjson(policy_pkg)),
        ("package/index.js", source_expected["policy-table/index.js"]),
        ("package/data/defaults.json", source_expected["policy-table/data/defaults.json"]),
    ],
}

def expected_tgz(members):
    tar_buf = io.BytesIO()
    with tarfile.open(fileobj=tar_buf, mode="w") as tar:
        for name, data in members:
            info = tarfile.TarInfo(name)
            info.size = len(data)
            info.mtime = MTIME
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            info.mode = 0o644
            tar.addfile(info, io.BytesIO(data))
    gz_buf = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", compresslevel=9, mtime=0, fileobj=gz_buf) as gz:
        gz.write(tar_buf.getvalue())
    return gz_buf.getvalue()

digests = {}
for filename, members in specs.items():
    path = MIRROR / filename
    data = path.read_bytes()
    if data != expected_tgz(members):
        fail(f"{filename} is not the required deterministic package tarball")
    with tarfile.open(fileobj=io.BytesIO(gzip.decompress(data)), mode="r:") as tar:
        infos = tar.getmembers()
        if [i.name for i in infos] != [m[0] for m in members]:
            fail(f"{filename} member order is wrong")
        for info, (_, payload) in zip(infos, members):
            if info.isdir():
                fail(f"{filename} contains directory entries")
            if (info.mtime, info.uid, info.gid, info.uname, info.gname, info.mode) != (MTIME, 0, 0, "", "", 0o644):
                fail(f"{filename} has wrong tar metadata for {info.name}")
            extracted = tar.extractfile(info).read()
            if extracted != payload:
                fail(f"{filename} payload mismatch for {info.name}")
    digests[filename] = {
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha512": base64.b64encode(hashlib.sha512(data).digest()).decode(),
    }

yarnrc_expected = 'yarn-offline-mirror "./mirror"\nyarn-offline-mirror-pruning true\n'
if (ROOT / ".yarnrc").read_text(encoding="utf-8") != yarnrc_expected:
    fail(".yarnrc content is wrong")

lock_expected = (
    "# THIS IS AN AUTOGENERATED FILE. DO NOT EDIT THIS FILE DIRECTLY.\n"
    "# yarn lockfile v1\n"
    "\n"
    '"@acme/edge-flags@1.2.0":\n'
    '  version "1.2.0"\n'
    f'  resolved "file:mirror/@acme-edge-flags-1.2.0.tgz#{digests["@acme-edge-flags-1.2.0.tgz"]["sha1"]}"\n'
    f'  integrity sha512-{digests["@acme-edge-flags-1.2.0.tgz"]["sha512"]}\n'
    "\n"
    '"@acme/policy-table@0.5.1":\n'
    '  version "0.5.1"\n'
    f'  resolved "file:mirror/@acme-policy-table-0.5.1.tgz#{digests["@acme-policy-table-0.5.1.tgz"]["sha1"]}"\n'
    f'  integrity sha512-{digests["@acme-policy-table-0.5.1.tgz"]["sha512"]}\n'
    "  dependencies:\n"
    '    "@acme/edge-flags" "1.2.0"\n'
)
if (ROOT / "yarn.lock").read_text(encoding="utf-8") != lock_expected:
    fail("yarn.lock content is wrong")

print("PASS")
Path("/logs/verifier/reward.txt").write_text("1\n")
PY
