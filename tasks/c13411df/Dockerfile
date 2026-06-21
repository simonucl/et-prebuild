# syntax=docker/dockerfile:1
# Author: storage-setup
# Description: Environment for storage usage summary exercise with pytest pre-installed.
# Help:
# This image provides:
# - /home/user/storage/volumes.csv with predefined content
# - /home/user/storage/logs directory (0755)
# - pytest available for test execution

FROM ubuntu:22.04

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    mkdir -p /home/user/storage/logs && \
    chmod 755 /home/user/storage/logs && \
    chmod 755 /home/user/storage

RUN cat <<'EOF' > /home/user/storage/volumes.csv
hostname,mount_point,disk_total_gb,disk_used_gb
alpha,/data,500,325
alpha,/backup,1000,100
bravo,/data,750,629
bravo,/logs,250,77
charlie,/var,600,420
EOF

RUN chmod 644 /home/user/storage/volumes.csv