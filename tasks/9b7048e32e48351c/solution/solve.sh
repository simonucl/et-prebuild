#!/bin/bash
set -euo pipefail

ROOT=/home/user/initramfs_lab/rootfs
OUT=/home/user/initramfs_lab/out
ARCHIVE="$OUT/recovery-initramfs.cpio.gz"
MANIFEST="$OUT/recovery-initramfs.manifest.json"

mkdir -p "$OUT"
rm -f "$ARCHIVE" "$MANIFEST"

chmod 0755 "$ROOT" "$ROOT/bin" "$ROOT/etc" "$ROOT/lib" "$ROOT/lib/modules" "$ROOT/lib/modules/6.8.0-edge" "$ROOT/sbin" "$ROOT/var" "$ROOT/var/lib" "$ROOT/var/lib/recovery"
chmod 0755 "$ROOT/init" "$ROOT/bin/busybox"
chmod 0644 "$ROOT/etc/recovery.conf" "$ROOT/lib/modules/6.8.0-edge/modules.dep" "$ROOT/var/lib/recovery/README"
touch -h -d @0 \
  "$ROOT" \
  "$ROOT/init" \
  "$ROOT/bin" \
  "$ROOT/bin/busybox" \
  "$ROOT/etc" \
  "$ROOT/etc/recovery.conf" \
  "$ROOT/lib" \
  "$ROOT/lib/modules" \
  "$ROOT/lib/modules/6.8.0-edge" \
  "$ROOT/lib/modules/6.8.0-edge/modules.dep" \
  "$ROOT/sbin" \
  "$ROOT/sbin/init" \
  "$ROOT/var" \
  "$ROOT/var/lib" \
  "$ROOT/var/lib/recovery" \
  "$ROOT/var/lib/recovery/README"

cd "$ROOT"
printf '%s\n' \
  . \
  init \
  bin \
  bin/busybox \
  etc \
  etc/recovery.conf \
  lib \
  lib/modules \
  lib/modules/6.8.0-edge \
  lib/modules/6.8.0-edge/modules.dep \
  sbin \
  sbin/init \
  var \
  var/lib \
  var/lib/recovery \
  var/lib/recovery/README \
  | cpio --quiet --create --format=newc --reproducible --owner=0:0 \
  | gzip -n > "$ARCHIVE"

python3 - <<'PY'
import gzip
import hashlib
import json
from pathlib import Path

archive = Path("/home/user/initramfs_lab/out/recovery-initramfs.cpio.gz")
payload = gzip.decompress(archive.read_bytes())
manifest = {
    "format": "newc+gzip",
    "member_count": 16,
    "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
    "uncompressed_sha256": hashlib.sha256(payload).hexdigest(),
    "root": "recovery-root",
}
Path("/home/user/initramfs_lab/out/recovery-initramfs.manifest.json").write_text(
    json.dumps(manifest, separators=(",", ":")) + "\n",
    encoding="utf-8",
)
PY
