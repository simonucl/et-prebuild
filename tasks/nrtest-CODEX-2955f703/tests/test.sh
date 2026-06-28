#!/bin/bash
set -u

mkdir -p /logs/verifier
REWARD=0
ROOT="${ROOT_PREFIX:-}"
SRC="$ROOT/home/user/release/src"
OUT="$ROOT/home/user/release/out"
ARCHIVE="$OUT/acme-widget-1.4.2-src.tar.gz"
SUMFILE="$OUT/acme-widget-1.4.2-src.tar.gz.sha256"
TMPDIR="$(mktemp -d)"

finish() {
  echo "$REWARD" > /logs/verifier/reward.txt
  rm -rf "$TMPDIR"
}
trap finish EXIT

fail() {
  echo "FAIL: $*" >&2
  exit 0
}

expect_file() {
  local path="$1"
  local expected="$2"
  [ -f "$path" ] || fail "missing source file: $path"
  printf '%b' "$expected" | cmp -s - "$path" || fail "source file was modified: $path"
}

[ -d "$SRC/acme-widget-1.4.2" ] || fail "source tree is missing"
[ -f "$ARCHIVE" ] || fail "archive is missing"
[ -f "$SUMFILE" ] || fail "checksum file is missing"

expect_file "$SRC/acme-widget-1.4.2/README.md" '# Acme Widget\n\nSmall command line widget used by release tests.\n'
expect_file "$SRC/acme-widget-1.4.2/LICENSE" 'MIT License\n\nCopyright 2024 Acme\n'
expect_file "$SRC/acme-widget-1.4.2/pyproject.toml" '[project]\nname = "acme-widget"\nversion = "1.4.2"\nrequires-python = ">=3.10"\n'
expect_file "$SRC/acme-widget-1.4.2/src/acme_widget/__init__.py" '__version__ = "1.4.2"\n'
expect_file "$SRC/acme-widget-1.4.2/src/acme_widget/cli.py" 'def main():\n    print("acme-widget 1.4.2")\n'
expect_file "$SRC/acme-widget-1.4.2/config/defaults.toml" '[defaults]\ncolor = "blue"\nretries = 3\n'
expect_file "$SRC/acme-widget-1.4.2/docs/changelog.md" '2024-01-10: release candidate\n2024-01-17: final release\n'
expect_file "$SRC/acme-widget-1.4.2/scripts/acme-widget" '#!/usr/bin/env bash\npython3 -m acme_widget.cli "$@"\n'
expect_file "$SRC/acme-widget-1.4.2/build/generated.bin" 'temporary build output\n'
expect_file "$SRC/acme-widget-1.4.2/dist/acme-widget-1.4.1.tar.gz" 'old package\n'
expect_file "$SRC/acme-widget-1.4.2/notes.tmp" 'scratch notes\n'
expect_file "$SRC/acme-widget-1.4.2/src/acme_widget/debug.tmp" 'print("debug")\n'
expect_file "$SRC/acme-widget-1.4.2/README.md~" 'editor backup\n'
expect_file "$SRC/acme-widget-1.4.2/.git/config" '[core]\n\trepositoryformatversion = 0\n'
expect_file "$SRC/acme-widget-1.4.2/.git/HEAD" 'ref: refs/heads/main\n'
expect_file "$SRC/acme-widget-1.4.2/.pytest_cache/CACHEDIR.TAG" 'Signature: 8a477f597d28d172789f06886806bc55\n'
[ "$(readlink "$SRC/acme-widget-1.4.2/docs/latest.md")" = "changelog.md" ] || fail "source symlink was modified"
[ "$(stat -c '%a' "$SRC/acme-widget-1.4.2/scripts/acme-widget")" = "755" ] || fail "source script mode was modified"

case "$(find "$OUT" -mindepth 1 -maxdepth 1 -printf '%f\n' | sort | tr '\n' ' ')" in
  "acme-widget-1.4.2-src.tar.gz acme-widget-1.4.2-src.tar.gz.sha256 ") ;;
  *) fail "output directory contains unexpected files" ;;
esac

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
  -cf - acme-widget-1.4.2 | gzip -n > "$TMPDIR/expected.tar.gz" || fail "could not build expected archive"

gzip -cd "$ARCHIVE" > "$TMPDIR/actual.tar" || fail "archive is not valid gzip"
gzip -cd "$TMPDIR/expected.tar.gz" > "$TMPDIR/expected.tar" || fail "expected archive is not valid gzip"

cmp -s "$TMPDIR/actual.tar" "$TMPDIR/expected.tar" || {
  echo "Archive listing produced by solver:" >&2
  tar -tvf "$ARCHIVE" >&2 || true
  fail "tar stream does not match the required normalized archive"
}

EXPECTED_SHA="$(sha256sum "$ARCHIVE" | awk '{print $1}')"
EXPECTED_LINE="$EXPECTED_SHA  acme-widget-1.4.2-src.tar.gz"
printf '%s\n' "$EXPECTED_LINE" | cmp -s - "$SUMFILE" || fail "checksum file content is incorrect"

tar -tf "$ARCHIVE" | grep -q '^acme-widget-1.4.2/docs/latest.md$' || fail "symlink entry is missing"
tar -tvf "$ARCHIVE" | grep -q ' acme-widget-1.4.2/docs/latest.md -> changelog.md$' || fail "docs/latest.md was not preserved as a relative symlink"

if tar -tf "$ARCHIVE" | grep -E '(^|/)(\.git|\.pytest_cache|build|dist)(/|$)|(\.tmp|~)$' >/dev/null; then
  fail "archive contains excluded content"
fi

REWARD=1
