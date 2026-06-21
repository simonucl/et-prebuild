# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update apt metadata and install required OS packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        procps \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Ensure the expected home directory exists and is writable at runtime
RUN mkdir -p /home/user && \
    chmod 0755 /home/user

# Environment variables
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PATH=/usr/local/bin:/usr/bin:/bin