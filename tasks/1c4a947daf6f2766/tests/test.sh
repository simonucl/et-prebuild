#!/bin/bash
set -u

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

def fail(msg):
    print(f"FAIL: {msg}")
    reward_file.parent.mkdir(parents=True, exist_ok=True)
    reward_file.write_text("0\n")
    sys.exit(0)

def ordered(obj, keys, label):
    if list(obj.keys()) != keys:
        fail(f"{label} keys are {list(obj.keys())}, expected {keys}")

root = Path(os.environ.get("TRSI_ROOT", "/"))
reward_file = Path(os.environ.get("TRSI_REWARD_FILE", "/logs/verifier/reward.txt"))
def ap(path):
    return root / path.lstrip("/")

repo = ap("/home/user/npm-lab/registry/@acme/edge-policy")
src = ap("/home/user/npm-lab/src/edge-policy")
tar_path = repo / "-" / "edge-policy-1.3.0.tgz"

expected_tree = sorted([
    "-",
    "-/edge-policy-1.3.0.tgz",
    "index.json",
    "manifest.json",
])
actual_tree = []
if not repo.exists():
    fail("registry directory is missing")
for root, dirs, files in os.walk(repo):
    rel_root = Path(root).relative_to(repo)
    for d in dirs:
        actual_tree.append(str((rel_root / d).as_posix()).lstrip("."))
    for f in files:
        actual_tree.append(str((rel_root / f).as_posix()).lstrip("."))
actual_tree = sorted(x for x in actual_tree if x)
if actual_tree != expected_tree:
    fail(f"registry contains unexpected entries: {actual_tree}")

tar_bytes = tar_path.read_bytes() if tar_path.exists() else fail("tarball is missing")
if len(tar_bytes) < 10 or tar_bytes[:2] != b"\x1f\x8b":
    fail("tarball is not gzip")
if tar_bytes[3] != 0:
    fail("gzip wrapper stores filename, comment, extra fields, or header crc")
if int.from_bytes(tar_bytes[4:8], "little") != 0:
    fail("gzip mtime is not zero")
if tar_bytes[8] != 2:
    fail("gzip stream was not written with maximum-compression header")

try:
    raw = gzip.decompress(tar_bytes)
except Exception as exc:
    fail(f"gzip stream cannot be decompressed: {exc}")

try:
    tf = tarfile.open(fileobj=io.BytesIO(raw), mode="r:")
    infos = tf.getmembers()
except Exception as exc:
    fail(f"tar stream cannot be read: {exc}")

expected_names = [
    "package/package.json",
    "package/README.md",
    "package/LICENSE",
    "package/dist/index.js",
    "package/dist/rules.json",
    "package/bin/edge-policy.js",
    "package/types/index.d.ts",
]
if [i.name for i in infos] != expected_names:
    fail(f"unexpected tar members or order: {[i.name for i in infos]}")
if any(not i.isfile() for i in infos):
    fail("tarball contains a non-regular-file member")

member_payloads = OrderedDict()
for info in infos:
    if info.mtime != 1782345600:
        fail(f"{info.name} has wrong mtime")
    if info.uid != 0 or info.gid != 0 or info.uname != "" or info.gname != "":
        fail(f"{info.name} does not use normalized numeric ownership")
    want_mode = 0o755 if info.name == "package/bin/edge-policy.js" else 0o644
    if info.mode != want_mode:
        fail(f"{info.name} mode is {oct(info.mode)}, expected {oct(want_mode)}")
    member_payloads[info.name] = tf.extractfile(info).read()

expected_package = OrderedDict([
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
package_bytes = json.dumps(expected_package, separators=(",", ":")).encode() + b"\n"
if member_payloads["package/package.json"] != package_bytes:
    fail("package/package.json content, key order, minification, or newline is wrong")

source_map = {
    "package/README.md": src / "README.md",
    "package/LICENSE": src / "LICENSE",
    "package/dist/index.js": src / "dist/index.js",
    "package/dist/rules.json": src / "dist/rules.json",
    "package/bin/edge-policy.js": src / "bin/edge-policy.js",
    "package/types/index.d.ts": src / "types/index.d.ts",
}
for name, path in source_map.items():
    if member_payloads[name] != path.read_bytes():
        fail(f"{name} content does not match the source tree")

sha1 = hashlib.sha1(tar_bytes).hexdigest()
integrity = "sha512-" + base64.b64encode(hashlib.sha512(tar_bytes).digest()).decode()
unpacked = sum(len(member_payloads[name]) for name in expected_names)

try:
    index_raw = (repo / "index.json").read_bytes()
    manifest_raw = (repo / "manifest.json").read_bytes()
except FileNotFoundError as exc:
    fail(f"missing metadata file: {exc}")
if not index_raw.endswith(b"\n") or index_raw.endswith(b"\n\n"):
    fail("index.json must have exactly one trailing newline")
if not manifest_raw.endswith(b"\n") or manifest_raw.endswith(b"\n\n"):
    fail("manifest.json must have exactly one trailing newline")
try:
    index = json.loads(index_raw, object_pairs_hook=OrderedDict)
    manifest = json.loads(manifest_raw, object_pairs_hook=OrderedDict)
except Exception as exc:
    fail(f"metadata JSON cannot be parsed: {exc}")
if index_raw != (json.dumps(index, separators=(",", ":")) + "\n").encode():
    fail("index.json is not minified or has unstable serialization")
if manifest_raw != (json.dumps(manifest, separators=(",", ":")) + "\n").encode():
    fail("manifest.json is not minified or has unstable serialization")

ordered(index, ["_id", "name", "dist-tags", "versions", "time"], "index.json")
if index["_id"] != "@acme/edge-policy" or index["name"] != "@acme/edge-policy":
    fail("index.json package identity is wrong")
if index["dist-tags"] != OrderedDict([("latest", "1.3.0")]):
    fail("index.json dist-tags are wrong")
if list(index["versions"].keys()) != ["1.3.0"]:
    fail("index.json versions must contain only 1.3.0")
v = index["versions"]["1.3.0"]
ordered(v, ["name", "version", "description", "license", "main", "types", "bin", "dist"], "index.json version object")
if list(v.items())[:7] != [
    ("name", "@acme/edge-policy"),
    ("version", "1.3.0"),
    ("description", "Offline edge policy compiler"),
    ("license", "MIT"),
    ("main", "dist/index.js"),
    ("types", "types/index.d.ts"),
    ("bin", OrderedDict([("edge-policy", "bin/edge-policy.js")])),
]:
    fail("index.json version metadata is wrong")
ordered(v["dist"], ["tarball", "shasum", "integrity", "unpackedSize"], "index.json dist object")
if v["dist"] != OrderedDict([
    ("tarball", "/@acme/edge-policy/-/edge-policy-1.3.0.tgz"),
    ("shasum", sha1),
    ("integrity", integrity),
    ("unpackedSize", unpacked),
]):
    fail("index.json dist metadata, checksums, or unpackedSize is wrong")
if index["time"] != OrderedDict([
    ("created", "2026-06-25T00:00:00.000Z"),
    ("modified", "2026-06-25T00:00:00.000Z"),
    ("1.3.0", "2026-06-25T00:00:00.000Z"),
]):
    fail("index.json time object is wrong")

ordered(manifest, ["package", "version", "tarball", "sha1", "integrity", "size_bytes", "files"], "manifest.json")
if list(manifest.items())[:6] != [
    ("package", "@acme/edge-policy"),
    ("version", "1.3.0"),
    ("tarball", "-/edge-policy-1.3.0.tgz"),
    ("sha1", sha1),
    ("integrity", integrity),
    ("size_bytes", len(tar_bytes)),
]:
    fail("manifest.json summary values are wrong")
expected_files = []
for name in expected_names:
    data = member_payloads[name]
    expected_files.append(OrderedDict([
        ("path", name),
        ("sha256", hashlib.sha256(data).hexdigest()),
        ("size_bytes", len(data)),
    ]))
if manifest["files"] != expected_files:
    fail("manifest.json files array, key order, hashes, sizes, or ordering is wrong")

reward_file.parent.mkdir(parents=True, exist_ok=True)
reward_file.write_text("1\n")
print("PASS")
PY
