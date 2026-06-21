# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Prepare environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Install packages and set up filesystem
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        iputils-ping && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create home directory and files
RUN mkdir -p /home/user && \
    chmod 0777 /home/user && \
    printf "127.0.0.1\n" > /home/user/target_ip.txt && \
    chmod 0644 /home/user/target_ip.txt

# Permissions adjustment specified in %environment
RUN chmod 755 /home/user