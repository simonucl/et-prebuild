# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author SomeAI
# Description: Environment for the 'compress rotated log files' task. Provides initial log files and empty archives directory.

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        xz-utils \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/storage/logs && \
    mkdir -p /home/user/archives && \
    printf "Dummy log 1\n" > /home/user/storage/logs/app-2023-09-01.log && \
    printf "Dummy log 2\n" > /home/user/storage/logs/app-2023-09-02.log && \
    printf "Dummy log 3\n" > /home/user/storage/logs/app-2023-09-03.log && \
    chmod 755 /home/user/storage /home/user/storage/logs && \
    chmod 777 /home/user/archives