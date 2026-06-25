#!/bin/bash
set -euo pipefail

src=/home/user/evidence/rootfs
out=/home/user/evidence/handoff
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

mkdir -p "$out"
find "$out" -mindepth 1 -maxdepth 1 -exec rm -rf {} +

tar \
  --format=posix \
  --sort=name \
  --mtime='@1782345600' \
  --owner=0 \
  --group=0 \
  --numeric-owner \
  --acls \
  --xattrs \
  --xattrs-include='user.*' \
  --sparse \
  --pax-option='delete=atime,delete=ctime,exthdr.name=%d/PaxHeaders/%f' \
  --transform='s,^\.$,edge-root,;s,^\./,edge-root/,' \
  -cf "$tmp/edge-root.pax.tar" \
  -C "$src" .

gzip -n -9 -c "$tmp/edge-root.pax.tar" > "$out/edge-root.pax.tar.gz"

python3 - <<'PY'
import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path

src = Path("/home/user/evidence/rootfs")
out = Path("/home/user/evidence/handoff")
archive = out / "edge-root.pax.tar.gz"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def xattrs(path: Path) -> dict[str, str]:
    names = subprocess.check_output(["getfattr", "--absolute-names", "-d", "-m", "user.*", str(path)], text=True, stderr=subprocess.DEVNULL)
    values = {}
    for line in names.splitlines():
        if line.startswith("user.") and "=" in line:
            key, raw = line.split("=", 1)
            values[key] = raw.strip('"')
    return dict(sorted(values.items()))

def has_backup_acl(path: Path) -> bool:
    acl = subprocess.check_output(["getfacl", "-cp", str(path)], text=True)
    return any(line == "user:backup:r--" for line in acl.splitlines())

paths = [src]
paths.extend(sorted((p for p in src.rglob("*")), key=lambda p: ("edge-root" if p == src else "edge-root/" + p.relative_to(src).as_posix()).encode()))
seen_inodes = {}
entries = []
for path in paths:
    rel = "edge-root" if path == src else "edge-root/" + path.relative_to(src).as_posix()
    st = path.lstat()
    mode = f"{stat.S_IMODE(st.st_mode):04o}"
    entry = {"path": rel, "type": "", "mode": mode}
    if stat.S_ISDIR(st.st_mode):
        entry["type"] = "dir"
    elif stat.S_ISLNK(st.st_mode):
        entry["type"] = "symlink"
        entry["target"] = os.readlink(path)
    elif stat.S_ISREG(st.st_mode):
        inode = (st.st_dev, st.st_ino)
        if inode in seen_inodes:
            entry["type"] = "hardlink"
            entry["hardlink_to"] = seen_inodes[inode]
        else:
            seen_inodes[inode] = rel
            entry["type"] = "file"
            entry["size"] = st.st_size
            entry["sha256"] = sha256_file(path)
            attrs = xattrs(path)
            if attrs:
                entry["xattrs"] = attrs
            if has_backup_acl(path):
                entry["acl"] = "user:backup:r--"
    else:
        raise SystemExit(f"unsupported file type: {path}")
    entries.append(entry)

manifest = {
    "archive": "edge-root.pax.tar.gz",
    "format": "posix-pax-gzip",
    "generated_at": "2026-06-25T00:00:00Z",
    "entries": entries,
    "archive_sha256": sha256_file(archive),
}
(out / "manifest.json").write_bytes(json.dumps(manifest, separators=(",", ":"), ensure_ascii=False).encode() + b"\n")
PY

archive_sha=$(sha256sum "$out/edge-root.pax.tar.gz" | awk '{print $1}')
manifest_sha=$(sha256sum "$out/manifest.json" | awk '{print $1}')
{
  printf '%s  edge-root.pax.tar.gz\n' "$archive_sha"
  printf '%s  manifest.json\n' "$manifest_sha"
} > "$out/SHA256SUMS"
