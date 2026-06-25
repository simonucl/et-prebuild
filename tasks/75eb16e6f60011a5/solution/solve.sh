#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import gzip
import hashlib
import io
import json
import shutil
import stat
from pathlib import Path

root = Path("/home/user/initramfs_lab")
source = root / "source"
out = root / "out"
epoch = 1714564800
members = [
    ".",
    "bin",
    "bin/busybox",
    "bin/sh",
    "etc",
    "etc/issue",
    "etc/mdev.conf",
    "init",
    "sbin",
    "sbin/init",
]

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def pad4(data: bytes) -> bytes:
    return data + (b"\0" * ((4 - (len(data) % 4)) % 4))

def align_buffer(buf: bytearray) -> None:
    buf.extend(b"\0" * ((4 - (len(buf) % 4)) % 4))

def header(name: str, mode: int, size: int, ino: int, nlink: int) -> bytes:
    fields = [
        "070701",
        f"{ino:08x}",
        f"{mode:08x}",
        f"{0:08x}",
        f"{0:08x}",
        f"{nlink:08x}",
        f"{epoch:08x}",
        f"{size:08x}",
        f"{0:08x}",
        f"{0:08x}",
        f"{0:08x}",
        f"{0:08x}",
        f"{len(name.encode()) + 1:08x}",
        f"{0:08x}",
    ]
    return "".join(fields).encode()

def add_record(buf: bytearray, name: str, mode: int, payload: bytes, ino: int, nlink: int) -> None:
    encoded_name = name.encode() + b"\0"
    buf.extend(header(name, mode, len(payload), ino, nlink))
    buf.extend(encoded_name)
    align_buffer(buf)
    buf.extend(payload)
    align_buffer(buf)

def member_mode(rel: str) -> tuple[int, bytes, int]:
    path = source if rel == "." else source / rel
    st = path.lstat()
    perm = stat.S_IMODE(st.st_mode)
    if stat.S_ISDIR(st.st_mode):
        return stat.S_IFDIR | 0o755, b"", 2
    if stat.S_ISLNK(st.st_mode):
        return stat.S_IFLNK | 0o777, path.readlink().as_posix().encode(), 1
    if stat.S_ISREG(st.st_mode):
        return stat.S_IFREG | perm, path.read_bytes(), 1
    raise SystemExit(f"unsupported source member: {rel}")

cpio = bytearray()
for ino, rel in enumerate(members, start=1):
    mode, payload, nlink = member_mode(rel)
    add_record(cpio, rel, mode, payload, ino, nlink)
add_record(cpio, "TRAILER!!!", stat.S_IFREG, b"", len(members) + 1, 1)
cpio_bytes = bytes(cpio)

gzbuf = io.BytesIO()
with gzip.GzipFile(filename="", mode="wb", fileobj=gzbuf, mtime=0, compresslevel=9) as fh:
    fh.write(cpio_bytes)
archive_bytes = gzbuf.getvalue()

shutil.rmtree(out, ignore_errors=True)
out.mkdir(parents=True)
(out / "rescue-initramfs.cpio.gz").write_bytes(archive_bytes)

manifest = {
    "archive": "rescue-initramfs.cpio.gz",
    "format": "newc-gzip",
    "generated_at": "2024-05-01T12:00:00Z",
    "members": members,
    "uncompressed_sha256": sha256(cpio_bytes),
    "archive_sha256": sha256(archive_bytes),
}
manifest_bytes = json.dumps(manifest, separators=(",", ":"), ensure_ascii=False).encode() + b"\n"
(out / "manifest.json").write_bytes(manifest_bytes)
(out / "SHA256SUMS").write_text(
    f"{sha256(archive_bytes)}  rescue-initramfs.cpio.gz\n"
    f"{sha256(manifest_bytes)}  manifest.json\n"
)
PY
