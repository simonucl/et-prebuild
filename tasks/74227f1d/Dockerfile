# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update package index and install Python, venv support, and pip
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest so the grader can run its test suite
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Prepare writable home directory expected by the tests
RUN mkdir -p /home/user/artifact-curator && \
    chmod -R 0777 /home/user

# Ensure correct permissions at runtime
RUN chmod 755 /home/user

ENV LC_ALL=C
ENV LANG=C
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH