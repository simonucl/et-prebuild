FROM ubuntu:22.04

# Labels
LABEL Author="edge-task-preparer"
LABEL Description="Environment for edge-deployment permissions task"

# Basic utilities and Python tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Latest pip and pytest for the grading harness
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# Ensure the expected home directory exists and is writable by any user
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Environment variables
ENV HOME=/home/user
ENV PATH=$HOME/.local/bin:$PATH

# Set working directory
WORKDIR /home/user

# Default action: drop into a shell
CMD ["/bin/bash"]