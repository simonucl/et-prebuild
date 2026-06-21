# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python, venv module and pip
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

# Install the exact pytest version required by the exercise
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest==7.2.0

# Ensure the expected home directory exists (owned by runtime user)
RUN mkdir -p /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# %help
# This container provides Python 3 with venv support and pytest 7.2.0 installed.