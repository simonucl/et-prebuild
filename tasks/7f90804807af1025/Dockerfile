FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends bash ca-certificates coreutils openssl python3 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user
WORKDIR /home/user/tuf_lab

RUN set -eu; \
    mkdir -p keys repository/targets/app repository/targets/bin repository/metadata; \
    openssl genpkey -algorithm ed25519 -out keys/root.ed25519.pem >/dev/null; \
    openssl genpkey -algorithm ed25519 -out keys/targets.ed25519.pem >/dev/null; \
    openssl genpkey -algorithm ed25519 -out keys/snapshot.ed25519.pem >/dev/null; \
    openssl genpkey -algorithm ed25519 -out keys/timestamp.ed25519.pem >/dev/null; \
    chmod 0600 keys/*.pem; \
    printf '%s\n' \
      'service: edge-api' \
      'listen: 127.0.0.1:8443' \
      'mode: offline' \
      'retry_budget: 5' \
      'features:' \
      '  audit_log: true' \
      '  dry_run: false' \
      > repository/targets/app/config.yaml; \
    printf '%s\n' \
      '#!/bin/sh' \
      'set -eu' \
      'case "${1:-}" in' \
      '  version) printf "edge-tool 2.4.1\n" ;;' \
      '  check) test -f /etc/edge/config.yaml && printf "ok\n" ;;' \
      '  *) printf "usage: edge-tool {version|check}\n" >&2; exit 64 ;;' \
      'esac' \
      > repository/targets/bin/edge-tool.sh; \
    chmod 0644 repository/targets/app/config.yaml; \
    chmod 0755 repository/targets/bin/edge-tool.sh; \
    printf '{"signed":{"_type":"root","version":2},"signatures":[]}\n' > repository/metadata/root.json; \
    printf '{"signed":{"_type":"targets","version":6},"signatures":[]}\n' > repository/metadata/targets.json; \
    printf '{"signed":{"_type":"snapshot","version":10},"signatures":[]}\n' > repository/metadata/snapshot.json; \
    printf '{"signed":{"_type":"timestamp","version":18},"signatures":[]}\n' > repository/metadata/timestamp.json; \
    printf 'old sidecar\n' > repository/metadata/README.old; \
    chown -R user:user /home/user/tuf_lab

USER user
