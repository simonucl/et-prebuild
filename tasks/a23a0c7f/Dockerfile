# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: AI-generated
# Description: Ubuntu 22.04 with pytest and a UID>=1000 user for assignment testing.

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV DEBIAN_FRONTEND=noninteractive

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        python3-pytest && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir --upgrade pytest && \
    if ! getent group user >/dev/null; then groupadd -g 1000 user; fi && \
    if ! id -u user >/dev/null 2>&1; then useradd -m -u 1000 -g 1000 -s /bin/bash user; fi && \
    chmod 755 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*