# syntax=docker/dockerfile:1
# Author: notifyd_setup
# Description: Base image for the notifyd configuration challenge (with pytest pre-installed).

FROM ubuntu:22.04

ENV PATH=/usr/local/bin:/usr/bin:/bin

# Environment-time chmod cannot be done in Dockerfile ENV, so included in build steps
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir pytest && \
    mkdir -p /home/user/.config/notifyd && \
    echo -n 'enabled=0' > /home/user/.config/notifyd/notifyd.conf && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/.config && \
    chmod 0755 /home/user/.config/notifyd && \
    chmod 0644 /home/user/.config/notifyd/notifyd.conf