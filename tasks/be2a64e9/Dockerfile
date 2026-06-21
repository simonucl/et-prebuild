# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# From %post
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    echo "Updating package lists and installing Python & pip..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-dev \
        curl \
        ca-certificates && \
    echo "Upgrading pip and installing pytest..." && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    echo "Creating /home/user with world-writable permissions..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    echo "Cleaning up apt caches..." && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# From %environment (converted appropriately)
RUN chmod 755 /home/user
ENV PATH="$PATH:/home/user/.local/bin"