#!/bin/bash
set -u

mkdir -p /logs/verifier
REWARD=0

python3 - <<'PY'
import gzip
import hashlib
import json
import stat
import sys
from pathlib import Path

archive = Path("/home/user/initramfs_lab/out/recovery-initramfs.cpio.gz")
manifest = Path("/home/user/initramfs_lab/out/recovery-initramfs.manifest.json")

expected = [
    (".", stat.S_IFDIR | 0o755, 0, b""),
    ("init", stat.S_IFREG | 0o755, 0, b"#!/bin/sh\nexport PATH=/bin:/sbin\nexec /bin/busybox sh\n"),
    ("bin", stat.S_IFDIR | 0o755, 0, b""),
    ("bin/busybox", stat.S_IFREG | 0o755, 0, b"#!/bin/sh\necho busybox rescue shell placeholder\n"),
    ("etc", stat.S_IFDIR | 0o755, 0, b""),
    ("etc/recovery.conf", stat.S_IFREG | 0o644, 0, b"mode=rescue\nroot=LABEL=RECOVERY\nconsole=ttyS0,115200n8\n"),
    ("lib", stat.S_IFDIR | 0o755, 0, b""),
    ("lib/modules", stat.S_IFDIR | 0o755, 0, b""),
    ("lib/modules/6.8.0-edge", stat.S_IFDIR | 0o755, 0, b""),
    ("lib/modules/6.8.0-edge/modules.dep", stat.S_IFREG | 0o644, 0, b"kernel/drivers/block/loop.ko:\nkernel/fs/squashfs/squashfs.ko: kernel/lib/decompress_unxz.ko\n"),
    ("sbin", stat.S_IFDIR | 0o755, 0, b""),
    ("sbin/init", stat.S_IFLNK | 0o777, 0, b"../init"),
    ("var", stat.S_IFDIR | 0o755, 0, b""),
    ("var/lib", stat.S_IFDIR | 0o755, 0, b""),
    ("var/lib/recovery", stat.S_IFDIR | 0o755, 0, b""),
    ("var/lib/recovery/README", stat.S_IFREG | 0o644, 0, b"Recovery image payload for the edge appliance.\n"),
]

def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)

if not archive.is_file():
    fail("archive is missing")
if not manifest.is_file():
    fail("manifest is missing")

raw = archive.read_bytes()
if len(raw) < 10 or raw[0:2] != b"\x1f\x8b" or raw[2] != 8:
    fail("archive is not gzip")
flags = raw[3]
mtime = int.from_bytes(raw[4:8], "little")
if flags != 0 or mtime != 0:
    fail("gzip header is not normalized")

try:
    payload = gzip.decompress(raw)
except Exception as exc:
    fail(f"gzip stream cannot be decompressed: {exc}")

def align4(n: int) -> int:
    return (n + 3) & ~3

entries = []
pos = 0
while True:
    if pos + 110 > len(payload):
        fail("cpio stream ended inside a header")
    header = payload[pos:pos + 110]
    pos += 110
    if header[:6] != b"070701":
        fail("cpio stream is not newc")
    fields = [int(header[6 + i * 8:14 + i * 8], 16) for i in range(13)]
    mode, uid, gid, nlink, mtime, filesize, namesize = fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[11]
    name_bytes = payload[pos:pos + namesize]
    pos = align4(pos + namesize)
    if not name_bytes.endswith(b"\0"):
        fail("cpio filename is not NUL-terminated")
    name = name_bytes[:-1].decode("utf-8")
    data = payload[pos:pos + filesize]
    pos = align4(pos + filesize)
    if name == "TRAILER!!!":
        break
    entries.append((name, mode, uid, gid, nlink, mtime, data))

if any(payload[pos:]):
    fail("cpio stream has nonzero trailing bytes after TRAILER")
if [entry[0] for entry in entries] != [entry[0] for entry in expected]:
    fail("archive member order or names are wrong")

for entry, exp in zip(entries, expected):
    name, mode, uid, gid, _nlink, mtime, data = entry
    exp_name, exp_mode, exp_mtime, exp_data = exp
    if name != exp_name:
        fail(f"unexpected member {name}")
    if mode != exp_mode:
        fail(f"{name} has wrong mode {mode:o}")
    if uid != 0 or gid != 0:
        fail(f"{name} has non-root uid/gid")
    if mtime != exp_mtime:
        fail(f"{name} has nonzero mtime")
    if data != exp_data:
        fail(f"{name} has wrong payload")

archive_hash = hashlib.sha256(raw).hexdigest()
payload_hash = hashlib.sha256(payload).hexdigest()
expected_manifest = (
    '{"format":"newc+gzip","member_count":16,'
    f'"archive_sha256":"{archive_hash}",'
    f'"uncompressed_sha256":"{payload_hash}",'
    '"root":"recovery-root"}\n'
)
actual_manifest = manifest.read_text(encoding="utf-8")
if actual_manifest != expected_manifest:
    fail("manifest content, key order, or trailing newline is wrong")
try:
    parsed = json.loads(actual_manifest)
except json.JSONDecodeError as exc:
    fail(f"manifest is not valid JSON: {exc}")
if parsed["archive_sha256"] != archive_hash or parsed["uncompressed_sha256"] != payload_hash:
    fail("manifest hashes do not match archive")

print("ok")
PY

if [ $? -eq 0 ]; then
  REWARD=1
fi

echo "$REWARD" > /logs/verifier/reward.txt
exit 0
