# syntax=docker/dockerfile:1
FROM ubuntu:22.04

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-venv python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/docs && \
    chmod -R 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH=/usr/bin:$PATH