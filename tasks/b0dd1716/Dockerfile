# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author backup-integrity-template
# Description Container prepared for backup-integrity verification task.
# This image contains the initial state for the backup-integrity exercise.
# A single file /home/user/backups/daily/important_data.tar.gz
# has been pre-placed with the exact SHA-256 digest required by the tests.
# Students must create a verification log as described in the assignment.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/backups/daily && \
    printf 'abc' > /home/user/backups/daily/important_data.tar.gz && \
    chmod 755 /home/user && \
    chmod -R 755 /home/user/backups && \
    chmod 644 /home/user/backups/daily/important_data.tar.gz