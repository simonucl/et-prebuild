# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install system dependencies, Python, pip, and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Prepare non-root user and required base directory structure
# ------------------------------------------------------------------
RUN set -eux && \
    groupadd -g 1000 user && \
    useradd -m -d /home/user -u 1000 -g 1000 user && \
    mkdir -p /home/user/app && \
    chown -R 1000:1000 /home/user && \
    chmod 755 /home/user

# ------------------------------------------------------------------
# Environment variables (from %environment)
# ------------------------------------------------------------------
ENV LC_ALL=C.UTF-8
ENV PATH=/home/user/.local/bin:$PATH

# ------------------------------------------------------------------
# Default command (from %runscript)
# ------------------------------------------------------------------
CMD ["/bin/bash"]