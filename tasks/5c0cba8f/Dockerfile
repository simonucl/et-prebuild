# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="AI Assistant"
LABEL Description="Ubuntu 22.04 base with Python, sqlite3, and pytest pre-installed for the compliance_audit task."

# Install system dependencies and Python tooling
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        sqlite3 && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure the expected home directory exists
RUN mkdir -p /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:$PATH