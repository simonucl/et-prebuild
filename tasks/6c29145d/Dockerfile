# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from %labels
LABEL Author="OpenAI ChatGPT" \
      Description="Environment for mock weather service configuration task with pytest pre-installed."

# Post-installation steps from %post
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    rm -rf /var/lib/apt/lists/*

# Environment setup from %environment
RUN chmod 755 /home/user

ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/local/bin:${PATH}"

# Help section (from %help)
# Environment for mock weather service configuration task with pytest pre-installed.