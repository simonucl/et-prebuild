# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author credential-rotation-setup
# Description "Container initial state for API credential rotation task"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/project

RUN cat > /home/user/project/.env <<'EOF'
# Application environment variables
SERVICE_URL="https://dev.example.com"
OLD_API_KEY="ABC123"
DEBUG=true
EOF

RUN chmod 777 /home/user/project && \
    chmod 666 /home/user/project/.env && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH