#!/bin/bash
set -euo pipefail

python3 - <<'PY'
from pathlib import Path
import gzip
import hashlib
import io
import json
import os
import tarfile

base = Path("/home/user/rootfs_lab")
src = base / "rootfs"
out = base / "handoff"
out.mkdir(parents=True, exist_ok=True)
for child in out.iterdir():
    if child.is_file() or child.is_symlink():
        child.unlink()
    elif child.is_dir():
        raise SystemExit(f"unexpected directory in handoff: {child}")

mtime = 1735689600
entries = [
    ("rootfs/", "dir", src, None),
    ("rootfs/etc/", "dir", src / "etc", None),
    ("rootfs/etc/edge-agent/", "dir", src / "etc/edge-agent", None),
    ("rootfs/etc/edge-agent/config.yaml", "file", src / "etc/edge-agent/config.yaml", None),
    ("rootfs/etc/edge-agent/policy.json", "symlink", src / "etc/edge-agent/policy.json", "../../usr/share/edge-agent/default-policy.json"),
    ("rootfs/usr/", "dir", src / "usr", None),
    ("rootfs/usr/local/", "dir", src / "usr/local", None),
    ("rootfs/usr/local/bin/", "dir", src / "usr/local/bin", None),
    ("rootfs/usr/local/bin/edge-agent", "file", src / "usr/local/bin/edge-agent", None),
    ("rootfs/usr/local/bin/edge-agent-current", "hardlink", src / "usr/local/bin/edge-agent-current", "rootfs/usr/local/bin/edge-agent"),
    ("rootfs/usr/share/", "dir", src / "usr/share", None),
    ("rootfs/usr/share/edge-agent/", "dir", src / "usr/share/edge-agent", None),
    ("rootfs/usr/share/edge-agent/default-policy.json", "file", src / "usr/share/edge-agent/default-policy.json", None),
    ("rootfs/var/", "dir", src / "var", None),
    ("rootfs/var/lib/", "dir", src / "var/lib", None),
    ("rootfs/var/lib/edge-agent/", "dir", src / "var/lib/edge-agent", None),
    ("rootfs/var/lib/edge-agent/state/", "dir", src / "var/lib/edge-agent/state", None),
    ("rootfs/var/lib/edge-agent/state/initial.db", "file", src / "var/lib/edge-agent/state/initial.db", None),
]

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

archive = out / "rootfs.tar.gz"
with archive.open("wb") as raw:
    with gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.GNU_FORMAT) as tf:
            for name, kind, path, link in entries:
                ti = tarfile.TarInfo(name)
                ti.mtime = mtime
                ti.uid = 0
                ti.gid = 0
                ti.uname = "root"
                ti.gname = "root"
                if kind == "dir":
                    ti.type = tarfile.DIRTYPE
                    ti.mode = 0o755
                    tf.addfile(ti)
                elif kind == "file":
                    data = path.read_bytes()
                    ti.type = tarfile.REGTYPE
                    ti.mode = path.stat().st_mode & 0o777
                    ti.size = len(data)
                    tf.addfile(ti, io.BytesIO(data))
                elif kind == "symlink":
                    ti.type = tarfile.SYMTYPE
                    ti.mode = 0o777
                    ti.linkname = link
                    tf.addfile(ti)
                elif kind == "hardlink":
                    ti.type = tarfile.LNKTYPE
                    ti.mode = path.stat().st_mode & 0o777
                    ti.linkname = link
                    tf.addfile(ti)

def file_meta(path: Path):
    data = path.read_bytes()
    return len(data), sha256_bytes(data)

edge_size, edge_sha = file_meta(src / "usr/local/bin/edge-agent")
config_size, config_sha = file_meta(src / "etc/edge-agent/config.yaml")
policy_size, policy_sha = file_meta(src / "usr/share/edge-agent/default-policy.json")
state_size, state_sha = file_meta(src / "var/lib/edge-agent/state/initial.db")

mtree_text = (
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
(out / "rootfs.mtree").write_text(mtree_text, encoding="utf-8")

manifest_entries = [
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
manifest = {
    "bundle": "rootfs.tar.gz",
    "mtree": "rootfs.mtree",
    "generated_at": "2025-01-01T00:00:00Z",
    "archive_sha256": sha256_bytes(archive.read_bytes()),
    "mtree_sha256": sha256_bytes((out / "rootfs.mtree").read_bytes()),
    "entries": manifest_entries,
}
(out / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n", encoding="utf-8")
PY
