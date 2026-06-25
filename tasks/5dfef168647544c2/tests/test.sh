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
  /app/handoff/fleet-agent-rootfs.sqsh \
  /app/handoff/manifest.json \
  /app/handoff/SHA256SUMS; do
  [ -f "$path" ] || fail "missing required file: $path"
done

actual_entries="$(cd /app/handoff && find . -mindepth 1 -maxdepth 1 -printf '%P\n' | LC_ALL=C sort)"
expected_entries=$'SHA256SUMS\nfleet-agent-rootfs.sqsh\nmanifest.json'
[ "$actual_entries" = "$expected_entries" ] || fail "handoff directory contains unexpected entries: [$actual_entries]"

mksquashfs /app/rootfs "$tmp/expected.sqsh" \
  -noappend \
  -comp xz \
  -b 131072 \
  -all-root \
  -all-time 1704067200 \
  -mkfs-time 1704067200 \
  -processors 1 \
  -no-progress \
  -wildcards \
  -e 'var/cache/fleet-agent/*' 'etc/fleet-agent/config.yaml.tmp' >/dev/null 2>"$tmp/mksquashfs.err" || {
    cat "$tmp/mksquashfs.err" >&2
    fail "could not build verifier reference SquashFS"
  }

cmp -s "$tmp/expected.sqsh" /app/handoff/fleet-agent-rootfs.sqsh || fail "fleet-agent-rootfs.sqsh is not the required normalized SquashFS image"

digest="$(sha256sum /app/handoff/fleet-agent-rootfs.sqsh | awk '{print $1}')"
bytes="$(stat -c '%s' /app/handoff/fleet-agent-rootfs.sqsh)"
printf '{"artifact":"fleet-agent-rootfs.sqsh","format":"squashfs","compression":"xz","block_size":131072,"created_at":"2024-01-01T00:00:00Z","sha256":"%s","bytes":%s}\n' \
  "$digest" "$bytes" > "$tmp/expected-manifest.json"
cmp -s "$tmp/expected-manifest.json" /app/handoff/manifest.json || fail "manifest content, key order, minification, digest, size, or trailing newline is incorrect"

printf '%s  fleet-agent-rootfs.sqsh\n' "$digest" > "$tmp/expected-SHA256SUMS"
cmp -s "$tmp/expected-SHA256SUMS" /app/handoff/SHA256SUMS || fail "SHA256SUMS has the wrong digest, spacing, filename, or trailing newline"

unsquashfs -d "$tmp/unpacked" -processors 1 /app/handoff/fleet-agent-rootfs.sqsh >/dev/null 2>"$tmp/unsquashfs.err" || {
  cat "$tmp/unsquashfs.err" >&2
  fail "generated SquashFS cannot be unpacked"
}

[ -f "$tmp/unpacked/etc/fleet-agent/config.yaml" ] || fail "config.yaml missing from image"
[ ! -e "$tmp/unpacked/etc/fleet-agent/config.yaml.tmp" ] || fail "transient config.yaml.tmp was included"
[ ! -e "$tmp/unpacked/var/cache/fleet-agent/cache.db" ] || fail "var/cache/fleet-agent contents were included"
[ -L "$tmp/unpacked/etc/fleet-agent/current.yaml" ] || fail "current.yaml symlink was not preserved"
[ "$(readlink "$tmp/unpacked/etc/fleet-agent/current.yaml")" = "config.yaml" ] || fail "current.yaml symlink target is wrong"
[ -x "$tmp/unpacked/usr/local/bin/fleet-agent" ] || fail "fleet-agent executable bit was not preserved"

reward=1
echo "$reward" > /logs/verifier/reward.txt
echo "ok"
