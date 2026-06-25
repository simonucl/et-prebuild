FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && apt-get install -y python3 ca-certificates && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    mkdir -p /app/rootfs/etc/edge-gateway /app/rootfs/usr/local/bin /app/rootfs/var/lib/edge-gateway /app/rootfs/run/edge-gateway /app/rootfs/tmp /app/oci-layout/blobs/sha256; \
    printf '%s\n' \
      'listen: "0.0.0.0:8443"' \
      'upstream: "https://control.internal"' \
      'retry_limit: 4' \
      'features:' \
      '  metrics: true' \
      '  audit_log: true' \
      > /app/rootfs/etc/edge-gateway/config.yaml; \
    printf '%s\n' \
      '#!/bin/sh' \
      'set -eu' \
      'exec echo "edge-gateway ${EDGE_GATEWAY_CONFIG:-/etc/edge-gateway/config.yaml}"' \
      > /app/rootfs/usr/local/bin/edge-gateway; \
    chmod 755 /app/rootfs/usr/local/bin/edge-gateway; \
    printf 'seeded-cache\n' > /app/rootfs/var/lib/edge-gateway/cache.db; \
    printf 'socket placeholder\n' > /app/rootfs/run/edge-gateway/control.sock; \
    printf 'temporary scratch\n' > /app/rootfs/tmp/build.log; \
    touch -d @1717286400 /app/rootfs/etc/edge-gateway/config.yaml /app/rootfs/usr/local/bin/edge-gateway /app/rootfs/var/lib/edge-gateway/cache.db /app/rootfs/run/edge-gateway/control.sock /app/rootfs/tmp/build.log; \
    printf '%s\n' '{"imageLayoutVersion":"1.0.0"}' > /app/oci-layout/oci-layout; \
    printf '%s\n' '{"schemaVersion":2,"manifests":[]}' > /app/oci-layout/index.json
