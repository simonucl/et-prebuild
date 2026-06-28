#!/bin/bash
set -euo pipefail

ROOT="${ROOT_PREFIX:-}"
SRC="$ROOT/home/user/release/src"
OUT="$ROOT/home/user/release/out"
ARCHIVE="acme-widget-1.4.2-src.tar.gz"

mkdir -p "$OUT"
rm -f "$OUT/$ARCHIVE" "$OUT/$ARCHIVE.sha256"

tar \
  --directory "$SRC" \
  --sort=name \
  --mtime='UTC 2024-01-01 00:00:00' \
  --owner=0 \
  --group=0 \
  --owner=root \
  --group=root \
  --pax-option=delete=atime,delete=ctime \
  --exclude='.git' \
  --exclude='.pytest_cache' \
  --exclude='build' \
  --exclude='dist' \
  --exclude='*.tmp' \
  --exclude='*~' \
  -cf - acme-widget-1.4.2 | gzip -n > "$OUT/$ARCHIVE"

(
  cd "$OUT"
  sha256sum "$ARCHIVE" > "$ARCHIVE.sha256"
)
