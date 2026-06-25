#!/bin/bash
set -u

mkdir -p /logs/verifier

if python3 - <<'PY'
import gzip
import hashlib
import io
import json
import stat
import sys
from pathlib import Path

root = Path("/home/user/initramfs_lab")
source = root / "source"
out = root / "out"
epoch = 1714564800
names = [
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
expected_source = {
    "init": (b"#!/bin/sh\nset -eu\nmount -t proc proc /proc 2>/dev/null || true\nexec /bin/sh\n", 0o755, "file"),
    "bin/busybox": (b'#!/bin/sh\nprintf "busybox rescue shell\\n"\n', 0o755, "file"),
    "bin/sh": (b"busybox", 0o777, "symlink"),
    "etc/issue": (b"ACME edge rescue initramfs\n", 0o644, "file"),
    "etc/mdev.conf": (b"ttyS0::respawn:/bin/sh\n", 0o644, "file"),
    "sbin/init": (b"../init", 0o777, "symlink"),
}

def fail(message: str) -> None:
    print("FAIL:", message, file=sys.stderr)
    raise SystemExit(1)

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def minjson(obj) -> bytes:
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False).encode() + b"\n"

def pad4(data: bytes) -> bytes:
    return data + (b"\0" * ((4 - (len(data) % 4)) % 4))

def align_buffer(buf: bytearray) -> None:
    buf.extend(b"\0" * ((4 - (len(buf) % 4)) % 4))

def header(name: str, mode: int, size: int, ino: int, nlink: int) -> bytes:
    return "".join([
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
    ]).encode()

def add_record(buf: bytearray, name: str, mode: int, payload: bytes, ino: int, nlink: int) -> None:
    buf.extend(header(name, mode, len(payload), ino, nlink))
    buf.extend(name.encode() + b"\0")
    align_buffer(buf)
    buf.extend(payload)
    align_buffer(buf)

def expected_mode_payload(rel: str):
    path = source if rel == "." else source / rel
    st = path.lstat()
    if stat.S_ISDIR(st.st_mode):
        return stat.S_IFDIR | 0o755, b"", 2
    if stat.S_ISLNK(st.st_mode):
        return stat.S_IFLNK | 0o777, path.readlink().as_posix().encode(), 1
    if stat.S_ISREG(st.st_mode):
        return stat.S_IFREG | stat.S_IMODE(st.st_mode), path.read_bytes(), 1
    fail(f"unsupported source member {rel}")

def build_expected_cpio() -> bytes:
    buf = bytearray()
    for ino, rel in enumerate(names, start=1):
        mode, payload, nlink = expected_mode_payload(rel)
        add_record(buf, rel, mode, payload, ino, nlink)
    add_record(buf, "TRAILER!!!", stat.S_IFREG, b"", len(names) + 1, 1)
    return bytes(buf)

def build_expected_gzip(data: bytes) -> bytes:
    outbuf = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=outbuf, mtime=0, compresslevel=9) as fh:
        fh.write(data)
    return outbuf.getvalue()

def read_newc(data: bytes):
    pos = 0
    records = []
    while True:
        hdr = data[pos:pos + 110]
        if len(hdr) != 110 or hdr[:6] != b"070701":
            fail("archive is not a valid newc stream")
        vals = [int(hdr[i:i + 8], 16) for i in range(6, 110, 8)]
        ino, mode, uid, gid, nlink, mtime, size, maj, minr, rmaj, rmin, namesize, check = vals
        pos += 110
        rawname = data[pos:pos + namesize]
        if not rawname.endswith(b"\0"):
            fail("newc filename is not NUL terminated")
        name = rawname[:-1].decode()
        pos += namesize
        pos += (4 - (pos % 4)) % 4
        payload = data[pos:pos + size]
        pos += size
        pos += (4 - (pos % 4)) % 4
        records.append((name, mode, uid, gid, nlink, mtime, size, maj, minr, rmaj, rmin, check, payload))
        if name == "TRAILER!!!":
            break
    if data[pos:] not in (b"",):
        fail("unexpected bytes after TRAILER!!!")
    return records

actual_source_files = sorted(str(p.relative_to(source)) for p in source.rglob("*") if p.is_file() or p.is_symlink())
if actual_source_files != sorted(expected_source):
    fail(f"source file set was modified: {actual_source_files}")
for rel, (payload, mode, kind) in expected_source.items():
    path = source / rel
    st = path.lstat()
    if kind == "file":
        if not stat.S_ISREG(st.st_mode) or path.read_bytes() != payload:
            fail(f"source file content changed: {rel}")
    else:
        if not stat.S_ISLNK(st.st_mode) or path.readlink().as_posix().encode() != payload:
            fail(f"source symlink changed: {rel}")
    if stat.S_IMODE(st.st_mode) != mode:
        fail(f"source mode changed for {rel}")

if sorted(p.name for p in out.iterdir() if p.is_file()) != ["SHA256SUMS", "manifest.json", "rescue-initramfs.cpio.gz"]:
    fail("out directory must contain exactly rescue-initramfs.cpio.gz, manifest.json, and SHA256SUMS")

archive = (out / "rescue-initramfs.cpio.gz").read_bytes()
if len(archive) < 10 or archive[:2] != b"\x1f\x8b":
    fail("archive is not gzip")
if archive[3] & 0x08:
    fail("gzip stream stores an original filename")
if int.from_bytes(archive[4:8], "little") != 0:
    fail("gzip mtime is not zero")

expected_cpio = build_expected_cpio()
expected_archive = build_expected_gzip(expected_cpio)
if archive != expected_archive:
    fail("rescue-initramfs.cpio.gz is not the required deterministic newc gzip archive")

try:
    uncompressed = gzip.decompress(archive)
except Exception as exc:
    fail(f"gzip decompression failed: {exc}")
if uncompressed != expected_cpio:
    fail("uncompressed cpio stream is incorrect")

records = read_newc(uncompressed)
if [r[0] for r in records] != names + ["TRAILER!!!"]:
    fail("newc member order is incorrect")
for record in records:
    name, mode, uid, gid, nlink, mtime, size, maj, minr, rmaj, rmin, check, payload = record
    if (uid, gid, mtime, maj, minr, rmaj, rmin, check) != (0, 0, epoch, 0, 0, 0, 0, 0):
        fail(f"newc metadata is incorrect for {name}")

manifest = {
    "archive": "rescue-initramfs.cpio.gz",
    "format": "newc-gzip",
    "generated_at": "2024-05-01T12:00:00Z",
    "members": names,
    "uncompressed_sha256": sha256(expected_cpio),
    "archive_sha256": sha256(expected_archive),
}
manifest_bytes = (out / "manifest.json").read_bytes()
if manifest_bytes != minjson(manifest):
    fail("manifest content, key order, minification, hashes, or trailing newline is incorrect")

checksums = (
    f"{sha256(expected_archive)}  rescue-initramfs.cpio.gz\n"
    f"{sha256(manifest_bytes)}  manifest.json\n"
).encode()
if (out / "SHA256SUMS").read_bytes() != checksums:
    fail("SHA256SUMS content is incorrect")
PY
then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
