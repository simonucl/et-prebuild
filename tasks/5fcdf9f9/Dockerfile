# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python tooling and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -qq && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Prepare initial filesystem state for the “asset list” exercise
# ------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user/site/static/utils && \
    mkdir -p /home/user/site/static/css && \
    mkdir -p /home/user/site/static/images && \
    chmod -R 777 /home/user && \
    chmod -R 777 /home/user/site && \
    printf 'console.log("App main");\n' > /home/user/site/static/app.js && \
    printf 'export function help() { return true; }\n' > /home/user/site/static/utils/helper.js && \
    printf 'body { margin: 0; }\n' > /home/user/site/static/css/style.css && \
    head -c 256 /dev/urandom > /home/user/site/static/images/logo.png

# ------------------------------------------------------------------
# Environment setup (from %environment)
# ------------------------------------------------------------------
RUN chmod 755 /home/user

# ------------------------------------------------------------------
# Labels (from %labels)
# ------------------------------------------------------------------
LABEL Author="asset-list-exercise" \
      Description="Base container for generate asset list task with initial static files."

# ------------------------------------------------------------------
# Run script information (from %runscript)
# ------------------------------------------------------------------
# This container is prepared for the asset-list exercise.
# Enter the container and work in /home/user/site.

WORKDIR /home/user/site