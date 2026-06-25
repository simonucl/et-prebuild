FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends bash python3 ca-certificates \
  && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
  mkdir -p /app/rootfs/etc/audit-agent /app/rootfs/usr/local/bin /app/rootfs/var/lib/audit-agent /app/rootfs/var/cache/audit-agent /app/oci/blobs/sha256; \
  printf 'server: https://collector.internal\nbatch_size: 128\nmode: strict\n' > /app/rootfs/etc/audit-agent/config.yaml; \
  printf 'server: https://old.example.invalid\n' > /app/rootfs/etc/audit-agent/config.yaml.bak; \
  ln -s config.yaml /app/rootfs/etc/audit-agent/current.yaml; \
  printf '#!/bin/sh\nset -eu\nexec echo audit-agent-ready\n' > /app/rootfs/usr/local/bin/audit-agent; \
  printf '{"cursor":"2024-01-01T00:00:00Z","seq":42}\n' > /app/rootfs/var/lib/audit-agent/state.json; \
  printf 'transient cache\n' > /app/rootfs/var/cache/audit-agent/cache.db; \
  chmod 0640 /app/rootfs/etc/audit-agent/config.yaml; \
  chmod 0644 /app/rootfs/etc/audit-agent/config.yaml.bak /app/rootfs/var/lib/audit-agent/state.json /app/rootfs/var/cache/audit-agent/cache.db; \
  chmod 0755 /app/rootfs/usr/local/bin/audit-agent; \
  printf '{"imageLayoutVersion":"1.0.0"}\n' > /app/oci/oci-layout; \
  printf '{"schemaVersion":2,"manifests":[]}\n' > /app/oci/index.json; \
  printf 'broken placeholder\n' > /app/oci/blobs/sha256/deadbeef
