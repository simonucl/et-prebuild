# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Apptainer Auto-Build"
LABEL Description="Base image with pytest and writable /home/user for the Kubernetes mini-operator task."

# Install Python, pip, and dependencies, then pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        ca-certificates \
        --no-install-recommends && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure correct permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV PATH="/home/user/.local/bin:${PATH}"

# Help:
# Base image with pytest and writable /home/user for the Kubernetes mini-operator task.