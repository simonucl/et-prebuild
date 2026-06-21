FROM ubuntu:22.04

# Labels
LABEL Author="observability-task-prep"
LABEL Description="Base image for the heartbeat-style metric collector exercise"

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Post installation
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        cron \
        ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/user

# Test that pytest is importable
RUN python3 -c "import pytest, sys; sys.exit(0)"

# Default command
CMD ["/bin/bash"]