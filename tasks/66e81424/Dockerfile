# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Apptainer build script"
LABEL Description="Environment for network-diagnostic heartbeat exercise"

# Post section: install packages and set up environment
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        iputils-ping \
        --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test harness
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Ensure baseline home directory exists and is writable
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Environment section
ENV PYTHONIOENCODING="utf-8"

# Ensure correct permissions at runtime
RUN chmod 755 /home/user