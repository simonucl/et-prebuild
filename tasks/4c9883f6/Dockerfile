FROM ubuntu:22.04

# Install Python, pip, and minimal utilities
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tar \
        gzip && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install pytest
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# Prepare initial workspace
RUN mkdir -p /home/user/ci_cd/logs && \
    printf 'Stage 1 completed\n' > /home/user/ci_cd/logs/stage1.log && \
    printf 'Stage 2 completed\n' > /home/user/ci_cd/logs/stage2.log && \
    printf 'Stage 3 completed\n' > /home/user/ci_cd/logs/stage3.log && \
    chmod 0644 /home/user/ci_cd/logs/stage*.log && \
    chmod -R 0755 /home/user/ci_cd && \
    mkdir -p /home/user/backups && \
    chmod 0777 /home/user/backups && \
    chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8