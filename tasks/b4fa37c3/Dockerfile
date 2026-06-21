# syntax=docker/dockerfile:1
# Author: AI_GPT
# Description: Base image for provisioning-log exercise; includes Python, pytest, and an empty /home/user workspace.
# Help:
# This container provides a minimal Ubuntu 22.04 environment with Python 3 and
# pytest pre-installed. It also sets up an empty, writable /home/user directory.

FROM ubuntu:22.04

LABEL Author="AI_GPT"
LABEL Description="Base image for provisioning-log exercise; includes Python, pytest, and an empty /home/user workspace."

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -qq && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

CMD ["bash"]