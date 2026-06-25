#!/bin/bash
set -u

mkdir -p /logs/verifier
reward=0
tmp="$(mktemp -d)"

cleanup() {
  rm -rf "$tmp"
}
trap cleanup EXIT

fail() {
  echo "FAIL: $*" >&2
  echo "$reward" > /logs/verifier/reward.txt
  exit 1
}

for path in \
  /app/handoff/rescue-initramfs.cpio.gz \
  /app/handoff/manifest.json \
  /app/handoff/SHA256SUMS; do
  [ -f "$path" ] || fail "missing required file: $path"
done

actual_entries="$(cd /app/handoff && find . -mindepth 1 -maxdepth 1 -printf '%P\n' | LC_ALL=C sort)"
expected_entries=$'SHA256SUMS\nmanifest.json\nrescue-initramfs.cpio.gz'
[ "$actual_entries" = "$expected_entries" ] || fail "handoff directory contains unexpected entries: [$actual_entries]"

mkdir -p "$tmp/root"
cp -a /app/initramfs-src/. "$tmp/root/"
rm -f "$tmp/root/etc/rescue/local.secret"
rm -rf "$tmp/root/var/log/rescue"
find "$tmp/root" -exec touch -h -d '@1709210096' {} +

(
  cd "$tmp/root"
  LC_ALL=C find . -mindepth 1 -printf '%P\0' | \
    LC_ALL=C sort -z | \
    cpio --null --create --format=newc --owner=0:0 --reproducible 2>/dev/null | \
    gzip -n -9 > "$tmp/expected.cpio.gz"
) || fail "could not build verifier reference initramfs"

cmp -s "$tmp/expected.cpio.gz" /app/handoff/rescue-initramfs.cpio.gz || fail "rescue-initramfs.cpio.gz is not the required normalized cpio.gz archive"

mkdir -p "$tmp/unpacked"
(
  cd "$tmp/unpacked"
  gzip -dc /app/handoff/rescue-initramfs.cpio.gz | cpio -id --quiet
) || fail "generated archive cannot be unpacked"

[ -x "$tmp/unpacked/init" ] || fail "init is missing or not executable"
[ -x "$tmp/unpacked/usr/bin/recovery" ] || fail "usr/bin/recovery is missing or not executable"
[ -x "$tmp/unpacked/bin/busybox" ] || fail "bin/busybox is missing or not executable"
[ -f "$tmp/unpacked/etc/rescue/config.env" ] || fail "config.env is missing"
[ ! -e "$tmp/unpacked/etc/rescue/local.secret" ] || fail "local.secret was included"
[ ! -e "$tmp/unpacked/var/log/rescue/boot.log" ] || fail "var/log/rescue contents were included"
[ -L "$tmp/unpacked/sbin/recovery" ] || fail "sbin/recovery symlink was not preserved"
[ "$(readlink "$tmp/unpacked/sbin/recovery")" = "../usr/bin/recovery" ] || fail "sbin/recovery symlink target is wrong"
[ -p "$tmp/unpacked/run/recovery.fifo" ] || fail "run/recovery.fifo FIFO was not preserved"

python3 - <<'PY' || fail "archive member metadata is incorrect"
import gzip
import stat
import sys
from pathlib import Path

data = gzip.decompress(Path("/app/handoff/rescue-initramfs.cpio.gz").read_bytes())
pos = 0
seen = []
while True:
    if data[pos:pos + 6] != b"070701":
        print("bad cpio magic", file=sys.stderr)
        sys.exit(1)
    fields = [int(data[pos + 6 + i * 8:pos + 14 + i * 8], 16) for i in range(13)]
    mode = fields[1]
    uid = fields[2]
    gid = fields[3]
    mtime = fields[5]
    filesize = fields[6]
    namesize = fields[11]
    pos += 110
    name = data[pos:pos + namesize - 1].decode()
    pos += namesize
    pos = (pos + 3) & ~3
    body = data[pos:pos + filesize]
    pos += filesize
    pos = (pos + 3) & ~3
    if name == "TRAILER!!!":
        break
    seen.append(name)
    if uid != 0 or gid != 0:
        print(f"{name}: uid/gid not normalized", file=sys.stderr)
        sys.exit(1)
    if mtime != 1709210096:
        print(f"{name}: mtime not normalized", file=sys.stderr)
        sys.exit(1)
    if name == "sbin/recovery":
        if not stat.S_ISLNK(mode) or body != b"../usr/bin/recovery":
            print("sbin/recovery is not the required symlink", file=sys.stderr)
            sys.exit(1)
    if name == "run/recovery.fifo" and not stat.S_ISFIFO(mode):
        print("run/recovery.fifo is not a FIFO", file=sys.stderr)
        sys.exit(1)

expected = [
    "bin",
    "bin/busybox",
    "etc",
    "etc/rescue",
    "etc/rescue/config.env",
    "init",
    "proc",
    "run",
    "run/recovery.fifo",
    "sbin",
    "sbin/recovery",
    "usr",
    "usr/bin",
    "usr/bin/recovery",
    "var",
    "var/log",
    "var/tmp",
    "var/tmp/runtime.note",
]
if seen != expected:
    print(f"unexpected archive order or file set: {seen}", file=sys.stderr)
    sys.exit(1)
PY

digest="$(sha256sum /app/handoff/rescue-initramfs.cpio.gz | awk '{print $1}')"
bytes="$(stat -c '%s' /app/handoff/rescue-initramfs.cpio.gz)"
entries="$(gzip -dc /app/handoff/rescue-initramfs.cpio.gz | cpio -it --quiet 2>/dev/null | wc -l | tr -d ' ')"
printf '{"artifact":"rescue-initramfs.cpio.gz","format":"cpio-newc","compression":"gzip-no-name","created_at":"2024-02-29T12:34:56Z","sha256":"%s","bytes":%s,"entries":%s}\n' \
  "$digest" "$bytes" "$entries" > "$tmp/expected-manifest.json"
cmp -s "$tmp/expected-manifest.json" /app/handoff/manifest.json || fail "manifest content, key order, digest, size, entry count, or trailing newline is incorrect"

printf '%s  rescue-initramfs.cpio.gz\n' "$digest" > "$tmp/expected-SHA256SUMS"
cmp -s "$tmp/expected-SHA256SUMS" /app/handoff/SHA256SUMS || fail "SHA256SUMS has the wrong digest, spacing, filename, or trailing newline"

reward=1
echo "$reward" > /logs/verifier/reward.txt
echo "ok"
