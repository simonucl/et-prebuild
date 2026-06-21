# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Basic development/runtime tools
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-venv \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create the non-privileged account “user”
RUN useradd -m -s /bin/bash user && \
    chmod 0755 /home/user

# Python testing framework
RUN --mount=type=cache,target=/root/.cache/pip python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# Environment variables
ENV PATH=$PATH:/home/user/.local/bin