# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: backup-task-initializer
# Description: Initial filesystem for docs backup task with pytest pre-installed.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && apt-get update -y && apt-get install -y --no-install-recommends python3 python3-pip
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/docs && mkdir -p /home/user/backups && mkdir -p /home/user/restore

RUN cat <<'EOF' > /home/user/docs/README.md
# Documentation

This is the README.
EOF

RUN cat <<'EOF' > /home/user/docs/architecture.md
# Architecture

System overview.
EOF

RUN cat <<'EOF' > /home/user/docs/user_guide.md
# User Guide

How to use the system.
EOF

RUN chmod -R 777 /home/user

RUN chmod 755 /home/user

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

CMD ["/bin/bash"]