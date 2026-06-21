# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python tooling
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest==8.1.1

# Prepare a writable workspace for the unprivileged test user
RUN mkdir -p /home/user && chmod 0777 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1

# Help (converted from %labels)
# Author: Container build automation
# Description: Apptainer image for the package-requirements normalisation exercise.

# Default runscript
CMD ["bash"]