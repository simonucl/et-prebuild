# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from %labels
LABEL Author="Generated for firewall rule task"
LABEL Description="Container prepared for Linux firewall rule exercise with pytest installed."

# Post section commands
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-wheel && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0755 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables from %environment
ENV PATH="$PATH:/home/user/.local/bin"

# Default command from %runscript
CMD ["/bin/bash"]

# %help
# This Apptainer container provides the environment for the firewall rule
# creation task. Pytest is installed, and /home/user exists for the student
# to work in.