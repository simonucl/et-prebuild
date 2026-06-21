# syntax=docker/dockerfile:1
# Author: Container setup for incident-42 task
# Description: Provides initial state for configuration patching exercise

FROM ubuntu:22.04

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    groupadd -g 1000 user || true && \
    useradd -m -d /home/user -u 1000 -g user user || true && \
    install -d -m 0755 /home/user/app/conf && \
    install -d -m 0755 /home/user/incident_fixes

RUN cat <<'EOF' > /home/user/app/conf/app.conf
# Application configuration
TIMEOUT=30
LOG_LEVEL=WARN
ENABLE_CACHE=true
EOF

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked chmod 0644 /home/user/app/conf/app.conf && \
    chown -R 1000:1000 /home/user && \
    chmod 755 /home/user && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH=/home/user/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

CMD echo "Container for incident-42 task. No default runscript actions defined."