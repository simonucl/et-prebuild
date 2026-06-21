FROM ubuntu:22.04

# Install Python, pip and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-privileged user and writable home directory
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -d /home/user -s /bin/bash user; \
    fi && \
    mkdir -p /home/user && \
    chmod 777 /home/user

# Set environment variables
ENV PATH=$PATH:/home/user/.local/bin

# Labels
LABEL Author="monitoring-platform-demo"
LABEL Description="Minimal base image for the monitoring-platform PoC exercise"