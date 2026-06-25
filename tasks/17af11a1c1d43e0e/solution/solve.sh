#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import gzip
import hashlib
import json
import os
import stat
from pathlib import Path

ROOT = Path("/app/rootfs")
OUT = Path("/app/handoff")
OUT.mkdir(parents=True, exist_ok=True)
ARCHIVE = OUT / "rescue-initramfs.cpio.gz"
FIXED_MTIME = 1714550400

EXCLUDE_FILES = {"etc/rescue/local.key"}
EXCLUDE_PREFIXES = ("var/cache/rescue/",)

def should_include(rel: str) -> bool:
    if rel in EXCLUDE_FILES:
        return False
    return not any(rel.startswith(prefix) for prefix in EXCLUDE_PREFIXES)

def header(namesize: int, filesize: int, mode: int, ino: int, nlink: int) -> bytes:
    fields = [
        "070701",
        f"{ino:08x}",
        f"{mode:08x}",
        "00000000",
        "00000000",
        f"{nlink:08x}",
        f"{FIXED_MTIME:08x}",
        f"{filesize:08x}",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        f"{namesize:08x}",
        "00000000",
    ]
    return "".join(fields).encode("ascii")

def append_padded(buf: bytearray, data: bytes) -> None:
    buf.extend(data)
    buf.extend(b"\0" * ((4 - (len(buf) % 4)) % 4))

entries = ["."]
for path in sorted(ROOT.rglob("*"), key=lambda p: p.relative_to(ROOT).as_posix()):
    rel = path.relative_to(ROOT).as_posix()
    if should_include(rel):
        entries.append(rel)

archive = bytearray()
for ino, rel in enumerate(entries, 1):
    path = ROOT if rel == "." else ROOT / rel
    st = os.lstat(path)
    mode = stat.S_IMODE(st.st_mode)
    data = b""
    nlink = 1
    if stat.S_ISDIR(st.st_mode):
        filetype = stat.S_IFDIR
        mode = mode or 0o755
        nlink = 2
    elif stat.S_ISLNK(st.st_mode):
        filetype = stat.S_IFLNK
        data = os.readlink(path).encode("utf-8")
    elif stat.S_ISREG(st.st_mode):
        filetype = stat.S_IFREG
        data = path.read_bytes()
    else:
        continue

    name = rel.encode("utf-8") + b"\0"
    archive.extend(header(len(name), len(data), filetype | mode, ino, nlink))
    append_padded(archive, name)
    append_padded(archive, data)

trailer = b"TRAILER!!!\0"
archive.extend(header(len(trailer), 0, stat.S_IFREG, len(entries) + 1, 1))
append_padded(archive, trailer)
raw = bytes(archive)

with gzip.GzipFile(filename="", mode="wb", fileobj=ARCHIVE.open("wb"), mtime=0, compresslevel=9) as gz:
    gz.write(raw)

digest = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
size = ARCHIVE.stat().st_size
(OUT / "SHA256SUMS").write_text(f"{digest}  rescue-initramfs.cpio.gz\n", encoding="utf-8")
(OUT / "manifest.json").write_text(
    json.dumps(
        {
            "artifact": "rescue-initramfs.cpio.gz",
            "format": "cpio-newc",
            "compression": "gzip",
            "created_at": "2024-05-01T08:00:00Z",
            "entries": len(entries) + 1,
            "sha256": digest,
            "bytes": size,
        },
        separators=(",", ":"),
    )
    + "\n",
    encoding="utf-8",
)
PY
