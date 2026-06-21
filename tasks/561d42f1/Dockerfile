# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------
# Install system packages and Python dependencies
# ------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        iputils-ping \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the testing harness
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------
# Prepare initial filesystem state expected by the automated tests
# ------------------------------------------------------------

# Ensure base home directory exists and is writable by any user
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Create the data directory and the required CSV file
RUN mkdir -p /home/user/data && \
    cat > /home/user/data/targets.csv <<'EOF'
hostname,description
127.0.0.1,local loopback
192.0.2.1,test unreachable host
EOF

# Set reasonable permissions
RUN chmod 0755 /home/user/data && \
    chmod 0644 /home/user/data/targets.csv

# ------------------------------------------------------------
# Metadata
# ------------------------------------------------------------
LABEL Author="OpenAI-ChatGPT" \
      Description="Environment for network reachability diagnostics task"

# ------------------------------------------------------------
# Help
# ------------------------------------------------------------
# This container provides the initial filesystem layout and software
# dependencies (Python, pytest, iputils-ping) required for the reachability
# diagnostics task.