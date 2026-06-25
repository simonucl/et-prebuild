#!/bin/bash
set -u

mkdir -p /logs/verifier

python3 - <<'PY'
import gzip
import hashlib
import json
import os
import stat
import sys
from pathlib import Path

ROOT = Path("/app/rootfs")
OUT = Path("/app/handoff")
ARCHIVE = OUT / "rescue-initramfs.cpio.gz"
FIXED_MTIME = 1714550400
EXPECTED_FILES = {"rescue-initramfs.cpio.gz", "manifest.json", "SHA256SUMS"}
EXCLUDE_FILES = {"etc/rescue/local.key"}
EXCLUDE_PREFIXES = ("var/cache/rescue/",)

def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)

def read_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except FileNotFoundError:
        fail(f"missing required file: {path}")

def require_source(path: str, data: bytes | None = None, mode: int | None = None) -> None:
    p = ROOT / path
    if not p.exists() and not p.is_symlink():
        fail(f"source rootfs was damaged; missing {path}")
    if data is not None and p.read_bytes() != data:
        fail(f"source rootfs was damaged; content changed for {path}")
    if mode is not None and stat.S_IMODE(os.lstat(p).st_mode) != mode:
        fail(f"source rootfs was damaged; mode changed for {path}")

require_source("init", b"#!/bin/sh\nmount -t proc proc /proc\nexec /usr/bin/rescue-init\n", 0o755)
require_source("bin/sh", b"#!/bin/sh\necho rescue shell\n", 0o755)
require_source("usr/bin/rescue-init", b"#!/bin/sh\necho starting rescue agent\n", 0o755)
require_source("etc/rescue/rescue.conf", b"RESCUE_MODE=offline\nROOT_DEVICE=LABEL=fleet-root\n", 0o644)
require_source("etc/rescue/authorized_keys", b"ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOfflineRescueKey operator@fleet\n", 0o600)
require_source("etc/rescue/local.key", b"temporary signing key that must not ship\n", 0o600)
require_source("var/cache/rescue/blob.cache", b"cache entry that must not ship\n")
require_source("var/lib/rescue/state", b"rescue-state=clean\nboot-count=0\n", 0o644)
require_source("lib/modules/6.8.0-rescue/kernel/drivers/net/fleetnet.ko", b"kernel-module-placeholder\n", 0o644)
if not (ROOT / "sbin/init").is_symlink() or os.readlink(ROOT / "sbin/init") != "../usr/bin/rescue-init":
    fail("source rootfs was damaged; sbin/init symlink is wrong")

if not OUT.is_dir():
    fail("missing /app/handoff directory")
actual_files = {p.name for p in OUT.iterdir() if p.is_file()}
if actual_files != EXPECTED_FILES:
    fail(f"handoff directory has unexpected file set: {sorted(actual_files)}")

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
expected_raw = bytes(archive)

actual_archive = read_bytes(ARCHIVE)
if len(actual_archive) < 10 or actual_archive[0:2] != b"\x1f\x8b" or actual_archive[2] != 8:
    fail("rescue-initramfs.cpio.gz is not a gzip-compressed archive")
gzip_flags = actual_archive[3]
if gzip_flags & 0b00011110:
    fail("gzip header contains optional filename, extra, comment, or header CRC fields")
if actual_archive[4:8] != b"\0\0\0\0":
    fail("gzip header mtime is not normalized to 0")

try:
    actual_raw = gzip.decompress(actual_archive)
except Exception as exc:
    fail(f"rescue-initramfs.cpio.gz is not valid gzip data: {exc}")
if actual_raw != expected_raw:
    fail("decompressed newc cpio payload is not the required reproducible archive")

def parse_newc(payload: bytes):
    pos = 0
    out = []
    while True:
        if pos + 110 > len(payload):
            fail("cpio payload ended inside a header")
        hdr = payload[pos:pos + 110]
        pos += 110
        if hdr[:6] != b"070701":
            fail("cpio payload is not newc format")
        vals = [int(hdr[i:i + 8], 16) for i in range(6, 110, 8)]
        ino, mode, uid, gid, nlink, mtime, filesize = vals[:7]
        namesize = vals[11]
        name = payload[pos:pos + namesize]
        pos += namesize
        pos += (-pos) % 4
        data = payload[pos:pos + filesize]
        pos += filesize
        pos += (-pos) % 4
        if not name.endswith(b"\0"):
            fail("cpio filename is not NUL terminated")
        text_name = name[:-1].decode("utf-8")
        out.append((text_name, ino, mode, uid, gid, nlink, mtime, data))
        if text_name == "TRAILER!!!":
            break
    return out

parsed = parse_newc(actual_raw)
names = [item[0] for item in parsed]
if names != entries + ["TRAILER!!!"]:
    fail(f"cpio entry order or file set is wrong: {names}")
for name, ino, mode, uid, gid, nlink, mtime, data in parsed:
    if uid != 0 or gid != 0:
        fail(f"{name} uid/gid is not normalized to 0")
    if mtime != FIXED_MTIME:
        fail(f"{name} mtime is not normalized")
if b"temporary signing key" in actual_raw or b"cache entry that must not ship" in actual_raw:
    fail("excluded secret or cache content was included in the archive")

digest = hashlib.sha256(actual_archive).hexdigest()
size = len(actual_archive)
expected_manifest = (
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
    + "\n"
).encode("utf-8")
if read_bytes(OUT / "manifest.json") != expected_manifest:
    fail("manifest content, key order, minification, digest, size, entry count, or trailing newline is incorrect")

expected_sums = f"{digest}  rescue-initramfs.cpio.gz\n".encode("ascii")
if read_bytes(OUT / "SHA256SUMS") != expected_sums:
    fail("SHA256SUMS has the wrong digest, spacing, filename, or trailing newline")
PY
status=$?

if [ "$status" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
exit "$status"
