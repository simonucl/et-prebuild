# syntax=docker/dockerfile:1
# Author: "Container build for diagnostic-bundle task"
# This image provides the initial state required for the
# “standard short-form diagnostic bundle” task. Pytest is pre-installed
# and the seed log file is located at /home/user/app/logs/app.log.

FROM ubuntu:22.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        iproute2 \
        procps \
        coreutils \
        util-linux && \
    pip3 install --no-cache-dir pytest

RUN install -d -m 0755 /home/user/app/logs

RUN cat > /home/user/app/logs/app.log <<'EOF'
2023-01-01 00:00:00 INFO Application started
2023-01-01 00:05:00 WARN No config file, using defaults
2023-01-01 00:10:00 INFO Service listening on port 8080
EOF

RUN chmod 0644 /home/user/app/logs/app.log

RUN chmod 0777 /home/user

ENV PATH="/usr/bin:${PATH}"