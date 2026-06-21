# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------
# Install Python, pip, and pytest
# ------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Create an unprivileged user (UID 1000) with home /home/user
# ------------------------------------------------------------
RUN useradd -m -s /bin/bash -u 1000 user

# ------------------------------------------------------------
# Prepare the initial file-system state expected by the test-suite
# ------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user/images/primary && \
    mkdir -p /home/user/images/backup && \
    dd if=/dev/zero of=/home/user/images/primary/golden.img bs=1024 count=256 status=none && \
    cp /home/user/images/primary/golden.img /home/user/images/backup/golden.img && \
    chmod 0777 /home/user/images/primary && \
    chmod 0777 /home/user/images/backup && \
    chown -R user:user /home/user

# ------------------------------------------------------------
# Environment setup (from %environment)
# ------------------------------------------------------------
RUN chmod 755 /home/user
ENV PATH="/home/user/.local/bin:${PATH}"

# ------------------------------------------------------------
# Help:
# This container provides Python 3 with pytest installed and
# prepares a predefined filesystem layout under /home/user.
# ------------------------------------------------------------