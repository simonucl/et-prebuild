#!/bin/bash
set -euo pipefail

mkdir -p /app/handoff
rm -f /app/handoff/fleet-agent-rootfs.sqsh /app/handoff/manifest.json /app/handoff/SHA256SUMS

mksquashfs /app/rootfs /app/handoff/fleet-agent-rootfs.sqsh \
  -noappend \
  -comp xz \
  -b 131072 \
  -all-root \
  -all-time 1704067200 \
  -mkfs-time 1704067200 \
  -processors 1 \
  -no-progress \
  -wildcards \
  -e 'var/cache/fleet-agent/*' 'etc/fleet-agent/config.yaml.tmp' >/dev/null

digest="$(sha256sum /app/handoff/fleet-agent-rootfs.sqsh | awk '{print $1}')"
bytes="$(stat -c '%s' /app/handoff/fleet-agent-rootfs.sqsh)"

printf '%s  fleet-agent-rootfs.sqsh\n' "$digest" > /app/handoff/SHA256SUMS
printf '{"artifact":"fleet-agent-rootfs.sqsh","format":"squashfs","compression":"xz","block_size":131072,"created_at":"2024-01-01T00:00:00Z","sha256":"%s","bytes":%s}\n' \
  "$digest" "$bytes" > /app/handoff/manifest.json
