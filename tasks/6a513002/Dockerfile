# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install required packages and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state for the assignment
RUN mkdir -p /home/user/mock/api && \
    printf '{"message":"Hello, integration test!"}' > /home/user/mock/api/greeting.json && \
    chmod 755 /home/user /home/user/mock /home/user/mock/api && \
    chmod 644 /home/user/mock/api/greeting.json

# Environment settings
ENV PYTHONUNBUFFERED=1