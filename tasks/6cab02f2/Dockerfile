# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="certificate-bundle-setup" \
      Description="Base image for certificate bundle exercise. Installs Python, pip, pytest and OpenSSL but leaves /home/user/profiling untouched so the agent can create the required artefacts during evaluation."

# Install system dependencies, Python tooling, and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        openssl \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 755 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH=/usr/local/bin:$PATH

# Default run behavior: execute provided command
ENTRYPOINT ["/bin/bash", "-c", "exec \"$@\"", "--"]
CMD []