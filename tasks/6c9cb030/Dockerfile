# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# %help
# Container for the QA-environment setup exercise.
# Provides Python 3, pip, python3-venv, and pytest 7.4.0.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        ca-certificates && \
    pip3 install --no-cache-dir pytest==7.4.0 && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    rm -rf /var/lib/apt/lists/*

# Environment settings
RUN chmod 755 /home/user
ENV PATH="/home/user/.local/bin:${PATH}"

# Default action: drop into a shell
CMD ["/bin/bash"]