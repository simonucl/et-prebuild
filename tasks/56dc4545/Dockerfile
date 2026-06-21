# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Base image for the firewall configuration exercise with pytest pre-installed.
LABEL Author="firewall-task" \
      Description="Base image for the firewall configuration exercise with pytest pre-installed."

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    mkdir -p /home/user && \
    chmod 755 /home/user && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Make sure user-installed Python tools are on PATH.
ENV PATH="/home/user/.local/bin:${PATH}"