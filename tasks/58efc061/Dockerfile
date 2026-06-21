# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# 1. Install required software
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        rsync && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# 2. Prepare initial directory structure & files
# ------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user && \
    mkdir -p /home/user/docs_local/images && \
    mkdir -p /home/user/docs_local/intro && \
    printf 'Hello, world.\n' > /home/user/docs_local/index.md && \
    printf '*.tmp\n' > /home/user/docs_local/.gitignore && \
    ln -s index.md /home/user/docs_local/README.md && \
    touch /home/user/docs_local/images/diagram.png && \
    printf 'Project overview.\n' > /home/user/docs_local/intro/overview.md && \
    mkdir -p /home/user/remote_server

# ------------------------------------------------------------------
# 3. Permissions
# ------------------------------------------------------------------
RUN chmod -R a+rwx /home/user && \
    chmod 755 /home/user

# ------------------------------------------------------------------
# Environment variables (from %environment)
# ------------------------------------------------------------------
ENV LC_ALL=C
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# ------------------------------------------------------------------
# %help
# This container provides a basic Ubuntu 22.04 environment with Python,
# pytest, and a prepared /home/user directory structure for documentation.
# ------------------------------------------------------------------