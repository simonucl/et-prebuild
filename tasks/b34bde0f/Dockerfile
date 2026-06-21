# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author text-encoding-regression-suite-prep

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        locales \
        libc-bin && \
    command -v iconv && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PYTHONUNBUFFERED=1