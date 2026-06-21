# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: benchmark-setup
# Description: Base container for benchmarking assignment (pytest included)

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 755 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

LABEL Author="benchmark-setup"
LABEL Description="Base container for benchmarking assignment (pytest included)"