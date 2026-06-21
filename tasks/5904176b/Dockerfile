# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer %labels
LABEL Author="IntegrationTaskSetup" \
      Description="Initial environment for API integration symbolic-link exercise."

# Install Python 3, pip, and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# File system setup
RUN set -e && \
    BASE="/home/user/projects/api_integration" && \
    mkdir -p "${BASE}/releases/v1" && \
    mkdir -p "${BASE}/releases/v2" && \
    mkdir -p "${BASE}/releases/v2/libs" && \
    mkdir -p "${BASE}/shared/config" && \
    mkdir -p "${BASE}/shared/libs" && \
    mkdir -p "${BASE}/libs/v1" && \
    mkdir -p "${BASE}/libs/v2" && \
    ln -sf "${BASE}/releases/v3" "${BASE}/current_release" && \
    mkdir -p /home/user && \
    chmod -R 0755 /home/user

# Environment variables from Apptainer %environment
ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Ensure permissions as in %environment
RUN chmod 755 /home/user

# Help (from Apptainer %help)
# Container for API integration deployment task. Pytest is installed.

# Default command (approximation of %runscript)
CMD ["bash"]