FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    coreutils \
    file \
    gzip \
    python3 \
    tar \
    && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    mkdir -p /app/rootfs/etc/edgecache /app/rootfs/usr/local/bin /app/rootfs/var/lib/edgecache /app/rootfs/var/cache/edgecache /app/oci/blobs/sha256; \
    printf '%s\n' \
      '[server]' \
      'listen = "127.0.0.1:8080"' \
      'cache_dir = "/var/lib/edgecache"' \
      '' \
      '[limits]' \
      'max_objects = 2048' \
      > /app/rootfs/etc/edgecache/edgecache.toml; \
    ln -s edgecache.toml /app/rootfs/etc/edgecache/current.toml; \
    printf '%s\n' \
      '#!/bin/sh' \
      'set -eu' \
      'exec /usr/bin/env printf "edgecache ready\\n"' \
      > /app/rootfs/usr/local/bin/edgecache; \
    chmod 0755 /app/rootfs/usr/local/bin/edgecache; \
    printf '{"objects":[{"key":"alpha","bytes":17},{"key":"beta","bytes":29}]}\n' > /app/rootfs/var/lib/edgecache/catalog.json; \
    printf 'temporary cache state\n' > /app/rootfs/var/cache/edgecache/index.db; \
    printf 'listen = "0.0.0.0:9999"\n' > /app/rootfs/etc/edgecache/edgecache.toml.tmp; \
    printf '{"schemaVersion":2,"manifests":[]}\n' > /app/oci/index.json; \
    printf '{"imageLayoutVersion":"1.0.0"}\n' > /app/oci/oci-layout
