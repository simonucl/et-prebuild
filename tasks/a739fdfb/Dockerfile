# syntax=docker/dockerfile:1
FROM ubuntu:22.04

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && apt-get update && apt-get install -y --no-install-recommends python3 python3-pip && rm -rf /var/lib/apt/lists/*
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/cicd/config

RUN cat > /home/user/cicd/config/build_settings.ini <<'EOF'
[pipeline]
name = core-build
version = 1.4.3-beta
runner = docker

[artifacts]
bucket = ci-build-artifacts
retention_days = 14

EOF

RUN chmod 644 /home/user/cicd/config/build_settings.ini
RUN chmod 755 /home/user

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8