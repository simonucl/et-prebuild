FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends bash coreutils findutils python3 squashfs-tools && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p \
      /app/rootfs/etc/fleet-agent \
      /app/rootfs/usr/local/bin \
      /app/rootfs/usr/share/fleet-agent/policies \
      /app/rootfs/var/lib/fleet-agent/state \
      /app/rootfs/var/cache/fleet-agent \
      /app/handoff && \
    printf '%s\n' \
      '#!/bin/sh' \
      'set -eu' \
      'exec /usr/bin/env printf "fleet-agent ready\n"' \
      > /app/rootfs/usr/local/bin/fleet-agent && \
    chmod 0755 /app/rootfs/usr/local/bin/fleet-agent && \
    printf '%s\n' \
      'agent:' \
      '  id: edge-west-17' \
      '  interval: 45s' \
      '  endpoint: https://collector.internal.example/v1/events' \
      'features:' \
      '  attest_boot: true' \
      '  ship_journal: true' \
      > /app/rootfs/etc/fleet-agent/config.yaml && \
    printf '%s\n' 'scratch config from last incident; do not ship' \
      > /app/rootfs/etc/fleet-agent/config.yaml.tmp && \
    ln -s config.yaml /app/rootfs/etc/fleet-agent/current.yaml && \
    printf '%s\n' \
      'package fleet.agent' \
      '' \
      'default allow = false' \
      '' \
      'allow if {' \
      '  input.node.trust == "hardware"' \
      '  input.report.signature == "valid"' \
      '}' \
      > /app/rootfs/usr/share/fleet-agent/policies/default.rego && \
    printf '%s\n' '{"last_success":"2026-06-20T03:14:15Z","sequence":1844}' \
      > /app/rootfs/var/lib/fleet-agent/state/last-run.json && \
    printf '%s\n' 'transient sqlite bytes would be here' \
      > /app/rootfs/var/cache/fleet-agent/cache.db && \
    find /app/rootfs -exec touch -h -d '2026-06-24 12:34:56 UTC' {} +
