# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python tooling
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Prepare writable workspace for the student
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Adjust permissions as specified in labels section
RUN chmod 755 /home/user

LABEL maintainer="release-manager-task" \
      description="Base container for rollout preparation task v1.2.3 – includes pytest and writable /home/user."