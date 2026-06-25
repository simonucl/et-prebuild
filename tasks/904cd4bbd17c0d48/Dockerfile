FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash ca-certificates coreutils findutils gzip python3 tar \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user

RUN set -eux; \
    root=/home/user/release_src/gateway-agent-2.7.0; \
    mkdir -p "$root/bin" "$root/docs" "$root/etc/gateway-agent" "$root/lib/systemd/system" "$root/.git/hooks" "$root/tmp"; \
    printf 'Gateway Agent 2.7.0\n===================\n\nOffline field gateway supervisor.\n' > "$root/README.md"; \
    printf 'Copyright 2024 Acme Edge Systems\nSPDX-License-Identifier: Apache-2.0\n' > "$root/LICENSE"; \
    printf '#!/usr/bin/env bash\nset -euo pipefail\nprintf "gateway-agent 2.7.0\\n"\n' > "$root/bin/gateway-agent"; \
    printf 'listen: "127.0.0.1:9443"\nspool_dir: "/var/lib/gateway-agent/spool"\nretry_seconds: 15\n' > "$root/etc/gateway-agent/config.yaml"; \
    printf '[Unit]\nDescription=Gateway Agent\nAfter=network-online.target\n\n[Service]\nExecStart=/usr/local/bin/gateway-agent --config /etc/gateway-agent/config.yaml\nRestart=on-failure\n\n[Install]\nWantedBy=multi-user.target\n' > "$root/lib/systemd/system/gateway-agent.service"; \
    printf '# Field Runbook\n\n1. Verify the service is active.\n2. Confirm the local spool is draining.\n' > "$root/docs/runbook.md"; \
    ln -s runbook.md "$root/docs/current"; \
    printf 'old generated backup - do not ship\n' > "$root/README.md~"; \
    printf 'temporary local note - do not ship\n' > "$root/tmp/operator-note.tmp"; \
    printf 'ref: refs/heads/main\n' > "$root/.git/HEAD"; \
    chmod 0755 "$root/bin/gateway-agent"; \
    chown -R user:user /home/user/release_src

USER user
WORKDIR /home/user
