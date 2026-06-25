FROM ubuntu:24.04

WORKDIR /home/user

RUN apt-get update && apt-get install -y \
    bash \
    coreutils \
    findutils \
    gzip \
    python3 \
    tar \
    && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    mkdir -p /home/user/rootfs_lab/rootfs/etc/edge-agent; \
    mkdir -p /home/user/rootfs_lab/rootfs/usr/local/bin; \
    mkdir -p /home/user/rootfs_lab/rootfs/usr/share/edge-agent; \
    mkdir -p /home/user/rootfs_lab/rootfs/var/lib/edge-agent/state; \
    mkdir -p /home/user/rootfs_lab/rootfs/.git/hooks; \
    mkdir -p /home/user/rootfs_lab/rootfs/tmp/cache; \
    printf 'listen: 127.0.0.1:9107\nmode: offline\npolicy: /etc/edge-agent/policy.json\n' > /home/user/rootfs_lab/rootfs/etc/edge-agent/config.yaml; \
    printf '#!/bin/sh\nset -eu\nexec printf "edge-agent offline\\\\n"\n' > /home/user/rootfs_lab/rootfs/usr/local/bin/edge-agent; \
    chmod 0755 /home/user/rootfs_lab/rootfs/usr/local/bin/edge-agent; \
    ln /home/user/rootfs_lab/rootfs/usr/local/bin/edge-agent /home/user/rootfs_lab/rootfs/usr/local/bin/edge-agent-current; \
    printf '{"rules":[{"name":"local-only","allow":["127.0.0.1/32","::1/128"]}],"default":"deny"}\n' > /home/user/rootfs_lab/rootfs/usr/share/edge-agent/default-policy.json; \
    ln -s ../../usr/share/edge-agent/default-policy.json /home/user/rootfs_lab/rootfs/etc/edge-agent/policy.json; \
    printf 'seeded-state-v1\ncheckpoint=42\n' > /home/user/rootfs_lab/rootfs/var/lib/edge-agent/state/initial.db; \
    chmod 0600 /home/user/rootfs_lab/rootfs/var/lib/edge-agent/state/initial.db; \
    printf 'do not package\n' > /home/user/rootfs_lab/rootfs/tmp/cache/debug.log; \
    printf 'stale metadata\n' > /home/user/rootfs_lab/rootfs/.git/config; \
    mkdir -p /home/user/rootfs_lab/handoff; \
    printf 'stale\n' > /home/user/rootfs_lab/handoff/rootfs.tar.gz; \
    printf 'stale\n' > /home/user/rootfs_lab/handoff/rootfs.mtree; \
    printf '{}\n' > /home/user/rootfs_lab/handoff/manifest.json
