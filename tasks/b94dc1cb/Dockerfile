# syntax=docker/dockerfile:1
# Base container for the “APP_PROFILING one-liner” exercise.
# Includes Python 3, pip, pytest, and pre-created user 'user' with /home/user.

FROM ubuntu:22.04

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel && \
    pip3 install --no-cache-dir --upgrade pytest && \
    if ! getent group 1000 >/dev/null; then groupadd -g 1000 user; fi && \
    if ! id -u 1000 >/dev/null 2>&1; then useradd -m -u 1000 -g 1000 -s /bin/bash user; fi && \
    mkdir -p /home/user && \
    chown -R 1000:1000 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

CMD ["/bin/bash"]

LABEL Author="Exercise Maintainer"
LABEL Description="Container environment for the APP_PROFILING one-line command exercise."