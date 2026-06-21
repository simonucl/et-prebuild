# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install required packages
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        openssh-client && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the checker
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare initial filesystem state expected by the task
# ------------------------------------------------------------------
# Home directory and .ssh folder for the non-privileged user
RUN mkdir -p /home/user/.ssh && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/.ssh

# Runtime environment setup
RUN chmod 755 /home/user

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8