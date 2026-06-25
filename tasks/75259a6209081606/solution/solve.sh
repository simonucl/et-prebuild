#!/bin/bash
set -euo pipefail

src=/app/initramfs-src
out=/app/handoff
epoch=1709210096
archive="$out/rescue-initramfs.cpio.gz"

mkdir -p "$out"
rm -f "$archive" "$out/manifest.json" "$out/SHA256SUMS"

tmp="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp"
}
trap cleanup EXIT

mkdir -p "$tmp/root"
cp -a "$src/." "$tmp/root/"
rm -f "$tmp/root/etc/rescue/local.secret"
rm -rf "$tmp/root/var/log/rescue"

find "$tmp/root" -exec touch -h -d "@$epoch" {} +

(
  cd "$tmp/root"
  LC_ALL=C find . -mindepth 1 -printf '%P\0' | \
    LC_ALL=C sort -z | \
    cpio --null --create --format=newc --owner=0:0 --reproducible 2>/dev/null | \
    gzip -n -9 > "$archive"
)

digest="$(sha256sum "$archive" | awk '{print $1}')"
bytes="$(stat -c '%s' "$archive")"
entries="$(gzip -dc "$archive" | cpio -it --quiet 2>/dev/null | wc -l | tr -d ' ')"

printf '%s  rescue-initramfs.cpio.gz\n' "$digest" > "$out/SHA256SUMS"
printf '{"artifact":"rescue-initramfs.cpio.gz","format":"cpio-newc","compression":"gzip-no-name","created_at":"2024-02-29T12:34:56Z","sha256":"%s","bytes":%s,"entries":%s}\n' \
  "$digest" "$bytes" "$entries" > "$out/manifest.json"
