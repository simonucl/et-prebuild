# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python 3, pip and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Prepare the initial workspace expected by the automated checker
# ------------------------------------------------------------------
# Directory layout:
# /home/user/workspace
# ├── file1.txt  (1 024 bytes)
# ├── file2.log  (2 048 bytes)
# └── logs/archive/file3.gz (4 096 bytes)
RUN set -e && \
    mkdir -p /home/user/workspace/logs/archive && \
    chmod 0777 /home/user /home/user/workspace /home/user/workspace/logs /home/user/workspace/logs/archive && \
    dd if=/dev/zero of=/home/user/workspace/file1.txt bs=1 count=1024 status=none && \
    dd if=/dev/zero of=/home/user/workspace/file2.log bs=1 count=2048 status=none && \
    dd if=/dev/zero of=/home/user/workspace/logs/archive/file3.gz bs=1 count=4096 status=none && \
    chmod 0644 /home/user/workspace/file1.txt && \
    chmod 0644 /home/user/workspace/file2.log && \
    chmod 0644 /home/user/workspace/logs/archive/file3.gz

# Ensure correct permissions on home directory
RUN chmod 755 /home/user

# ------------------------------------------------------------------
# Environment variables
# ------------------------------------------------------------------
ENV PYTHONIOENCODING=UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# ------------------------------------------------------------------
# Labels
# ------------------------------------------------------------------
LABEL Author="devsecops-task-preparer"
LABEL Description="Container for disk-usage policy enforcement task (pytest included)"