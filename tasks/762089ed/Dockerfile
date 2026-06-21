# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# %post section
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Prepare writable home directory expected by the tests
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# %labels section
RUN chmod 755 /home/user

LABEL Author="task-preparer" \
      Description="Container image for firewall rule creation exercise. Includes pytest and a writable /home/user directory."