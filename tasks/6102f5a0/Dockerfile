# syntax=docker/dockerfile:1
FROM ubuntu:22.04

LABEL Author="FinOps-Container-Builder" \
      Description="Environment for FinOps cron-scheduling task (pytest included)."

# Environment variables from %environment
ENV PATH="/usr/local/bin:${PATH}"

# Install required tools and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        cron \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Set up directories and permissions
RUN set -e && \
    mkdir -p /home/user/finops && \
    chmod 777 /home/user /home/user/finops

# Create the helper script
RUN cat >/home/user/finops/cleanup_stale_resources.sh <<'EOSCRIPT'
#!/usr/bin/env bash
echo "Cleaning up stale resources..."
EOSCRIPT

# Make the script executable
RUN chmod 755 /home/user/finops/cleanup_stale_resources.sh

# Ensure cron directories and permissions
RUN set -e && \
    mkdir -p /var/spool/cron/crontabs && \
    chmod 1730 /var/spool/cron/crontabs && \
    chgrp crontab /var/spool/cron/crontabs

# Clean up APT caches
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get clean && \
    rm -rf /var/lib/apt/lists/*