FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    bash \
    coreutils \
    dpkg-dev \
    file \
    findutils \
    gzip \
    python3 \
    xz-utils \
  && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
  mkdir -p /home/user/apt-lab/packages /home/user/apt-lab/repo; \
  mkdir -p /tmp/pkg-agent/DEBIAN /tmp/pkg-agent/usr/bin /tmp/pkg-agent/etc/acme; \
  printf 'Package: acme-edge-agent\nVersion: 1.4.0\nArchitecture: amd64\nMaintainer: Acme Edge Ops <edge-ops@example.com>\nInstalled-Size: 18\nDepends: libc6 (>= 2.39), acme-edge-rules (>= 2026.6-1)\nSection: admin\nPriority: optional\nDescription: Acme edge node supervisor\n Controls local edge services and reports health state.\n' > /tmp/pkg-agent/DEBIAN/control; \
  printf '#!/bin/sh\nset -eu\nprintf "acme-edge-agent 1.4.0\\n"\n' > /tmp/pkg-agent/usr/bin/acme-edge-agent; \
  chmod 0755 /tmp/pkg-agent/usr/bin/acme-edge-agent; \
  printf 'channel=stable\nfleet=edge-prod\n' > /tmp/pkg-agent/etc/acme/agent.conf; \
  dpkg-deb --build --root-owner-group /tmp/pkg-agent /home/user/apt-lab/packages/acme-edge-agent_1.4.0_amd64.deb; \
  mkdir -p /tmp/pkg-rules/DEBIAN /tmp/pkg-rules/usr/share/acme-edge-rules; \
  printf 'Package: acme-edge-rules\nVersion: 2026.6-1\nArchitecture: amd64\nMaintainer: Acme Edge Ops <edge-ops@example.com>\nInstalled-Size: 9\nDepends: \nSection: net\nPriority: optional\nDescription: Acme edge routing rule pack\n Static routing rules for offline edge nodes.\n' > /tmp/pkg-rules/DEBIAN/control; \
  printf '{"rules":[{"name":"default-deny","priority":1000},{"name":"allow-health","priority":10}]}\n' > /tmp/pkg-rules/usr/share/acme-edge-rules/rules.json; \
  dpkg-deb --build --root-owner-group /tmp/pkg-rules /home/user/apt-lab/packages/acme-edge-rules_2026.6-1_amd64.deb; \
  rm -rf /tmp/pkg-agent /tmp/pkg-rules; \
  mkdir -p /home/user/apt-lab/repo/dists/stable/main/binary-amd64 /home/user/apt-lab/repo/pool/main/a/acme-edge-agent /home/user/apt-lab/repo/pool/main/a/acme-edge-rules; \
  cp /home/user/apt-lab/packages/acme-edge-agent_1.4.0_amd64.deb /home/user/apt-lab/repo/pool/main/a/acme-edge-agent/acme-edge-agent_1.3.9_amd64.deb; \
  printf 'stale package index\n' > /home/user/apt-lab/repo/dists/stable/main/binary-amd64/Packages; \
  gzip -c /home/user/apt-lab/repo/dists/stable/main/binary-amd64/Packages > /home/user/apt-lab/repo/dists/stable/main/binary-amd64/Packages.gz; \
  printf 'Origin: stale\n' > /home/user/apt-lab/repo/dists/stable/Release; \
  printf '{"status":"stale"}\n' > /home/user/apt-lab/repo/repo-manifest.json; \
  chown -R root:root /home/user/apt-lab
