# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Apptainer Task Preparer"
LABEL Description="Base container for the pre-update diagnostic task with pytest pre-installed."

# Post section: install dependencies and set up environment
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Ensure correct permissions on home directory at runtime
RUN chmod 755 /home/user

# Default command
CMD ["bash"]