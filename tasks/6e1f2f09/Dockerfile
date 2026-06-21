# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Maintainer: network-automation-task
# Description: Initial container for connectivity assessment exercise

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        iputils-ping && \
    pip3 install --no-cache-dir pytest && \
    if ! id -u user >/dev/null 2>&1; then \
        useradd -m -d /home/user user; \
    fi && \
    mkdir -p /home/user && \
    chown -R user:user /home/user && \
    printf '127.0.0.1\nlocalhost\n198.51.100.1\n' > /home/user/targets.txt && \
    chmod 644 /home/user/targets.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH=/home/user/.local/bin:$PATH