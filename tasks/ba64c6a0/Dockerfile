# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Post section
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -u 1000 -s /bin/bash user && \
    chown -R 1000:1000 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment section
RUN chmod 755 /home/user
ENV PATH="/home/user/.local/bin:${PATH}"