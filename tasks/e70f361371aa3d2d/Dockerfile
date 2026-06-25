FROM ubuntu:24.04

WORKDIR /home/user

RUN apt-get update && apt-get install -y \
    bash \
    ca-certificates \
    coreutils \
    findutils \
    git \
    gzip \
    python3 \
    tar \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user

RUN set -eux; \
  mkdir -p /home/user/release/source /home/user/release/receiver.git; \
  chown -R user:user /home/user/release; \
  git -C /home/user/release/source init -b main; \
  git -C /home/user/release/source config user.name "ACME Release Bot"; \
  git -C /home/user/release/source config user.email "release-bot@internal.example"; \
  mkdir -p /home/user/release/source/config /home/user/release/source/scripts /home/user/release/source/assets; \
  printf '%s\n' '# Edge Collector' '' 'Offline edge telemetry collector.' > /home/user/release/source/README.md; \
  printf '%s\n' '[collector]' 'interval_seconds = 60' 'endpoint = "https://edge.internal.example/v1/events"' > /home/user/release/source/config/collector.toml; \
  printf '%s\n' '#!/usr/bin/env bash' 'set -euo pipefail' 'echo "edge-collector 1.8.0"' > /home/user/release/source/scripts/collect.sh; \
  chmod 0755 /home/user/release/source/scripts/collect.sh; \
  python3 -c 'from pathlib import Path; Path("/home/user/release/source/assets/probe.dat").write_bytes(bytes([0,1,2,3,5,8,13,21,34,55,89,144,233]))'; \
  git -C /home/user/release/source add .; \
  GIT_AUTHOR_DATE='2024-03-01T10:00:00Z' GIT_COMMITTER_DATE='2024-03-01T10:00:00Z' git -C /home/user/release/source commit -m 'Release edge collector 1.8.0'; \
  git -C /home/user/release/source tag v1.8.0; \
  git -C /home/user/release/source switch -c release/v1.9; \
  printf '%s\n' '[collector]' 'interval_seconds = 30' 'endpoint = "https://edge.internal.example/v2/events"' 'spool_dir = "/var/lib/edge-collector/spool"' > /home/user/release/source/config/collector.toml; \
  printf '%s\n' 'rules:' '  - id: cpu-pressure' '    threshold: 0.82' '  - id: queue-depth' '    threshold: 900' > /home/user/release/source/config/rules.yaml; \
  printf '%s\n' '# Edge Collector' '' 'Offline edge telemetry collector.' '' 'Version 1.9 adds queue-depth routing rules.' > /home/user/release/source/README.md; \
  git -C /home/user/release/source add .; \
  GIT_AUTHOR_DATE='2024-04-01T09:15:00Z' GIT_COMMITTER_DATE='2024-04-01T09:15:00Z' git -C /home/user/release/source commit -m 'Add 1.9 routing policy'; \
  printf '%s\n' '#!/usr/bin/env bash' 'set -euo pipefail' 'exec "${EDGE_COLLECTOR_BIN:-/usr/lib/edge-collector/collector}" --config /etc/edge-collector/collector.toml "$@"' > /home/user/release/source/scripts/collect.sh; \
  chmod 0755 /home/user/release/source/scripts/collect.sh; \
  python3 -c 'from pathlib import Path; Path("/home/user/release/source/assets/probe.dat").write_bytes(bytes([0,255,16,239,32,223,48,207,64,191,80,175,96,159,112,143,128]))'; \
  printf '%s\n' 'edge-collector v1.9.0' '=====================' '' '- Adds routing policy support.' '- Updates the probe payload used by smoke tests.' > /home/user/release/source/CHANGELOG.md; \
  git -C /home/user/release/source add .; \
  GIT_AUTHOR_DATE='2024-04-02T16:40:00Z' GIT_COMMITTER_DATE='2024-04-02T16:40:00Z' git -C /home/user/release/source commit -m 'Finalize 1.9 release payload'; \
  git -C /home/user/release/source tag v1.9.0; \
  git -C /home/user/release/receiver.git init --bare; \
  git -C /home/user/release/source push /home/user/release/receiver.git main:refs/heads/main v1.8.0; \
  git -C /home/user/release/receiver.git symbolic-ref HEAD refs/heads/main; \
  mkdir -p /home/user/release/handoff; \
  chown -R user:user /home/user/release

USER user
