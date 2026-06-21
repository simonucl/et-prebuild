# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author label from Apptainer definition
LABEL Author="Apptainer Task Setup"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create an unprivileged user "user" with home directory /home/user
RUN groupadd -g 1000 user && \
    useradd -m -d /home/user -s /bin/bash -u 1000 -g user user && \
    chown -R user:user /home/user

# Permissions setup from %environment
RUN chmod 755 /home/user

# Environment variables from %environment
ENV PATH="/home/user/.local/bin:${PATH}"
ENV HOME="/home/user"