# syntax=docker/dockerfile:1
# Equivalent Dockerfile

# Base image (converted from localimage ./ubuntu_22.04.sif)
FROM ubuntu:22.04

# Help text from %help (added as comments)
# Author: example
# Version: 1.0
# Description: Environment for release-packaging exercise (pytest included)

# Environment variables from %environment
ENV PATH="/home/user/.local/bin:${PATH}"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        passwd && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -u 1000 user && \
    RELEASE_DIR=/home/user/releases/v1.0 && \
    mkdir -p "$RELEASE_DIR/bin" "$RELEASE_DIR/config" && \
    echo "Project v1.0 — release notes." > "$RELEASE_DIR/README.md" && \
    printf '#!/usr/bin/env bash\necho '\''Starting v1.0'\''\n' > "$RELEASE_DIR/bin/start.sh" && \
    chmod 755 "$RELEASE_DIR/bin/start.sh" && \
    printf 'mode=production\nversion=1.0\n' > "$RELEASE_DIR/config/settings.conf" && \
    mkdir -p /home/user/releases_packages && \
    chown -R user:user /home/user && \
    chmod 755 /home/user /home/user/releases /home/user/releases/v1.0 \
        /home/user/releases/v1.0/bin /home/user/releases/v1.0/config \
        /home/user/releases_packages && \
    chmod 644 "$RELEASE_DIR/README.md" "$RELEASE_DIR/config/settings.conf"