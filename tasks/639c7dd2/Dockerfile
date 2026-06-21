# syntax=docker/dockerfile:1
FROM ubuntu:22.04

LABEL Maintainer="AI-generated definition file for backup integrity task"

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m pip install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare initial filesystem state expected by the grader
# ------------------------------------------------------------------

# Create user home hierarchy
RUN set -e && \
    mkdir -p /home/user/data && \
    mkdir -p /home/user/reports

# Set permissions
RUN set -e && \
    chmod 755 /home/user/data && \
    chmod 777 /home/user/reports

# Create the empty backup file with correct permissions
RUN set -e && \
    touch /home/user/data/backup.tar.gz && \
    chmod 644 /home/user/data/backup.tar.gz