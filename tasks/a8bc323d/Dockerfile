# syntax=docker/dockerfile:1
FROM ubuntu:22.04

LABEL Author="Container build for jq one-liner validation task"
LABEL Description="Provides jq, pytest, and pre-populated /home/user environment for the agent."

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    echo "Updating package lists and installing required packages..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        jq \
        python3 \
        python3-pip

RUN --mount=type=cache,target=/root/.cache/pip echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir pytest

RUN echo "Creating directory structure..." && \
    mkdir -p /home/user/storage && \
    mkdir -p /home/user/reports && \
    echo "Setting directory permissions to 0755..." && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/storage && \
    chmod 0755 /home/user/reports

RUN echo "Adding initial disks.json inventory..." && \
    cat <<'EOF' > /home/user/storage/disks.json
[
  { "name": "sda", "size_gb": 950 },
  { "name": "sdb", "size_gb": 1200 },
  { "name": "sdc", "size_gb": 500 }
]
EOF

RUN echo "Setting file permissions to 0644..." && \
    chmod 0644 /home/user/storage/disks.json

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked echo "Cleanup apt caches..." && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user