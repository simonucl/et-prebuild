# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: network-engineering-task-setup
# Description: Container image for network optimisation task; provides initial state and pytest

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/netops && \
    chmod 755 /home/user/netops

RUN cat > /home/user/netops/interfaces.cfg <<'EOF'
interface=eth0
mtu=1500
state=up
EOF

RUN chmod 644 /home/user/netops/interfaces.cfg

LABEL Author="network-engineering-task-setup" \
      Description="Container image for network optimisation task; provides initial state and pytest"