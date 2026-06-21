# syntax=docker/dockerfile:1
# Converted from Apptainer definition file
FROM ubuntu:22.04

# Labels
LABEL Author="Container setup for webdev_venv exercise"
LABEL Description="Ubuntu 22.04 base with Python, venv support, and pytest installed."

# Install system packages and Python tools
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment settings
ENV PATH=/usr/bin:$PATH

# Apply permissions from %environment (chmod cannot be in ENV)
RUN chmod 755 /home/user

# Equivalent of %runscript
# Container for the webdev_venv exercise. Run your commands inside /home/user.