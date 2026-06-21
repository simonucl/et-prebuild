# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Post section: install dependencies and set up environment
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0755 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH="/usr/local/bin:/usr/local/sbin:${PATH}"

# Ensure permissions on home directory
RUN chmod 755 /home/user

# Help / runscript information
# This container provides the environment for the incident-response exercise.
# Invoke your own scripts or an interactive shell as needed.

CMD echo "This container provides the environment for the incident-response exercise." && \
    echo "Invoke your own scripts or an interactive shell as needed."