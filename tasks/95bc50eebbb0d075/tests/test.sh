#!/bin/bash
set -euo pipefail

mkdir -p /logs/verifier

if python3 - <<'PY'
from pathlib import Path
import gzip
import hashlib
import json
import stat
import tarfile

base = Path("/home/user/rootfs_lab")
src = base / "rootfs"
out = base / "handoff"
archive = out / "rootfs.tar.gz"
mtree = out / "rootfs.mtree"
manifest_path = out / "manifest.json"
mtime = 1735689600

def fail(msg):
    raise AssertionError(msg)

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

if not out.is_dir():
    fail("handoff directory is missing")
names = sorted(p.name for p in out.iterdir())
if names != ["manifest.json", "rootfs.mtree", "rootfs.tar.gz"]:
    fail(f"handoff contains unexpected entries: {names}")
for p in [archive, mtree, manifest_path]:
    if not p.is_file():
        fail(f"{p} is not a regular file")

gz = archive.read_bytes()
if len(gz) < 10 or gz[:2] != b"\x1f\x8b":
    fail("rootfs.tar.gz is not gzip")
if int.from_bytes(gz[4:8], "little") != 0:
    fail("gzip header mtime is not zero")
if gz[3] & 0x08:
    fail("gzip header stores an original filename")

expected_order = [
    "rootfs",
    "rootfs/etc",
    "rootfs/etc/edge-agent",
    "rootfs/etc/edge-agent/config.yaml",
    "rootfs/etc/edge-agent/policy.json",
    "rootfs/usr",
    "rootfs/usr/local",
    "rootfs/usr/local/bin",
    "rootfs/usr/local/bin/edge-agent",
    "rootfs/usr/local/bin/edge-agent-current",
    "rootfs/usr/share",
    "rootfs/usr/share/edge-agent",
    "rootfs/usr/share/edge-agent/default-policy.json",
    "rootfs/var",
    "rootfs/var/lib",
    "rootfs/var/lib/edge-agent",
    "rootfs/var/lib/edge-agent/state",
    "rootfs/var/lib/edge-agent/state/initial.db",
]
source_by_member = {
    "rootfs/etc/edge-agent/config.yaml": src / "etc/edge-agent/config.yaml",
    "rootfs/usr/local/bin/edge-agent": src / "usr/local/bin/edge-agent",
    "rootfs/usr/share/edge-agent/default-policy.json": src / "usr/share/edge-agent/default-policy.json",
    "rootfs/var/lib/edge-agent/state/initial.db": src / "var/lib/edge-agent/state/initial.db",
}
with gzip.open(archive, "rb") as gzf:
    with tarfile.open(fileobj=gzf, mode="r:") as tf:
        members = tf.getmembers()
        if [m.name for m in members] != expected_order:
            fail(f"tar member order is wrong: {[m.name for m in members]}")
        for m in members:
            if m.mtime != mtime:
                fail(f"{m.name} has wrong mtime")
            if (m.uid, m.gid, m.uname, m.gname) != (0, 0, "root", "root"):
                fail(f"{m.name} has wrong owner metadata")
            if m.isdir():
                if not m.isdir() or (m.mode & 0o777) != 0o755:
                    fail(f"{m.name} is not a 0755 directory")
            elif m.name == "rootfs/etc/edge-agent/policy.json":
                if not m.issym() or m.linkname != "../../usr/share/edge-agent/default-policy.json" or (m.mode & 0o777) != 0o777:
                    fail("policy.json is not the required symlink")
            elif m.name == "rootfs/usr/local/bin/edge-agent-current":
                if not m.islnk() or m.linkname != "rootfs/usr/local/bin/edge-agent":
                    fail("edge-agent-current is not stored as the required hardlink")
                if (m.mode & 0o777) != 0o755:
                    fail("hardlink has wrong mode")
            elif m.name in source_by_member:
                data = tf.extractfile(m).read()
                source = source_by_member[m.name]
                if data != source.read_bytes():
                    fail(f"{m.name} content differs from source")
                if (m.mode & 0o777) != (source.stat().st_mode & 0o777):
                    fail(f"{m.name} mode differs from source")
            else:
                fail(f"unexpected non-directory member {m.name}")

def file_meta(path: Path):
    data = path.read_bytes()
    return len(data), sha256_bytes(data)

config_size, config_sha = file_meta(src / "etc/edge-agent/config.yaml")
edge_size, edge_sha = file_meta(src / "usr/local/bin/edge-agent")
policy_size, policy_sha = file_meta(src / "usr/share/edge-agent/default-policy.json")
state_size, state_sha = file_meta(src / "var/lib/edge-agent/state/initial.db")

expected_mtree = (
    "#mtree\n"
    "/set uid=0 gid=0 time=1735689600\n"
    ". type=dir mode=0755\n"
    "etc type=dir mode=0755\n"
    "etc/edge-agent type=dir mode=0755\n"
    f"etc/edge-agent/config.yaml type=file mode=0644 size={config_size} sha256={config_sha}\n"
    "etc/edge-agent/policy.json type=link mode=0777 link=../../usr/share/edge-agent/default-policy.json\n"
    "usr type=dir mode=0755\n"
    "usr/local type=dir mode=0755\n"
    "usr/local/bin type=dir mode=0755\n"
    f"usr/local/bin/edge-agent type=file mode=0755 size={edge_size} sha256={edge_sha} nlink=2\n"
    f"usr/local/bin/edge-agent-current type=file mode=0755 size={edge_size} sha256={edge_sha} nlink=2\n"
    "usr/share type=dir mode=0755\n"
    "usr/share/edge-agent type=dir mode=0755\n"
    f"usr/share/edge-agent/default-policy.json type=file mode=0644 size={policy_size} sha256={policy_sha}\n"
    "var type=dir mode=0755\n"
    "var/lib type=dir mode=0755\n"
    "var/lib/edge-agent type=dir mode=0755\n"
    "var/lib/edge-agent/state type=dir mode=0755\n"
    f"var/lib/edge-agent/state/initial.db type=file mode=0600 size={state_size} sha256={state_sha}\n"
)
if mtree.read_text(encoding="utf-8") != expected_mtree:
    fail("rootfs.mtree content is not the required mtree specification")

manifest_text = manifest_path.read_text(encoding="utf-8")
if not manifest_text.endswith("\n") or manifest_text.endswith("\n\n"):
    fail("manifest.json must have exactly one trailing newline")
manifest = json.loads(manifest_text)
expected_entries = [
    {"path": "rootfs/", "type": "dir", "mode": "0755"},
    {"path": "rootfs/etc/", "type": "dir", "mode": "0755"},
    {"path": "rootfs/etc/edge-agent/", "type": "dir", "mode": "0755"},
    {"path": "rootfs/etc/edge-agent/config.yaml", "type": "file", "mode": "0644", "size": config_size, "sha256": config_sha},
    {"path": "rootfs/etc/edge-agent/policy.json", "type": "symlink", "mode": "0777", "link": "../../usr/share/edge-agent/default-policy.json"},
    {"path": "rootfs/usr/", "type": "dir", "mode": "0755"},
    {"path": "rootfs/usr/local/", "type": "dir", "mode": "0755"},
    {"path": "rootfs/usr/local/bin/", "type": "dir", "mode": "0755"},
    {"path": "rootfs/usr/local/bin/edge-agent", "type": "file", "mode": "0755", "size": edge_size, "sha256": edge_sha, "nlink": 2},
    {"path": "rootfs/usr/local/bin/edge-agent-current", "type": "hardlink", "mode": "0755", "link": "rootfs/usr/local/bin/edge-agent", "size": edge_size, "sha256": edge_sha, "nlink": 2},
    {"path": "rootfs/usr/share/", "type": "dir", "mode": "0755"},
    {"path": "rootfs/usr/share/edge-agent/", "type": "dir", "mode": "0755"},
    {"path": "rootfs/usr/share/edge-agent/default-policy.json", "type": "file", "mode": "0644", "size": policy_size, "sha256": policy_sha},
    {"path": "rootfs/var/", "type": "dir", "mode": "0755"},
    {"path": "rootfs/var/lib/", "type": "dir", "mode": "0755"},
    {"path": "rootfs/var/lib/edge-agent/", "type": "dir", "mode": "0755"},
    {"path": "rootfs/var/lib/edge-agent/state/", "type": "dir", "mode": "0755"},
    {"path": "rootfs/var/lib/edge-agent/state/initial.db", "type": "file", "mode": "0600", "size": state_size, "sha256": state_sha},
]
expected_manifest = {
    "bundle": "rootfs.tar.gz",
    "mtree": "rootfs.mtree",
    "generated_at": "2025-01-01T00:00:00Z",
    "archive_sha256": sha256_bytes(archive.read_bytes()),
    "mtree_sha256": sha256_bytes(mtree.read_bytes()),
    "entries": expected_entries,
}
expected_text = json.dumps(expected_manifest, separators=(",", ":")) + "\n"
if manifest_text != expected_text:
    fail("manifest.json content, key order, hashes, or trailing newline is incorrect")

os_linked = (src / "usr/local/bin/edge-agent").stat().st_ino == (src / "usr/local/bin/edge-agent-current").stat().st_ino
if not os_linked:
    fail("source executable hardlink relationship was modified")
PY
then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
