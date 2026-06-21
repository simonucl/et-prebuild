# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from %labels
LABEL Author="Container Prep" \
      Description="Environment for the Container Image Inventory task with pytest pre-installed."

# Post section: install packages, prepare filesystem
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/images && \
    touch /home/user/images/ubuntu_latest.sif && \
    touch /home/user/images/alpine_3.18.sif && \
    touch /home/user/images/node_18.sif && \
    chmod -R a+rwX /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment setup
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# Ensure /home/user has correct permissions at runtime
RUN chmod 755 /home/user

# Help section (as comments)
# Environment for the Container Image Inventory task with pytest pre-installed.
# Provides Python 3, pip, pytest, and placeholder .sif images under /home/user/images.