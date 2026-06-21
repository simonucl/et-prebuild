# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Container Build Script" \
      Description="Apptainer image for the diagnostics bundle exercise"

# Update package lists and install Python tooling
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-wheel && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure correct permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:${PATH}"

# Set working directory
WORKDIR /home/user

# Default command (from %runscript)
CMD echo "Diagnostics exercise container. Launching shell..." && exec /bin/bash "$@"