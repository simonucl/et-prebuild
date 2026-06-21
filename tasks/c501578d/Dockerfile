# syntax=docker/dockerfile:1
# Converted from Apptainer definition file
FROM ubuntu:22.04

# System packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Directory layout
RUN mkdir -p /home/user/api_configs

# Configuration files
RUN cat > /home/user/api_configs/dev.json <<'JSON'
{
  "base_url": "https://dev.example.internal/api",
  "token": "dev-token"
}
JSON

RUN cat > /home/user/api_configs/staging.json <<'JSON'
{
  "base_url": "https://staging.example.internal/api",
  "token": "staging-token"
}
JSON

RUN cat > /home/user/api_configs/prod.json <<'JSON'
{
  "base_url": "https://api.example.com",
  "token": "prod-token"
}
JSON

# Permissions
RUN chmod 0755 /home/user/api_configs && \
    chmod 0644 /home/user/api_configs/*.json && \
    chmod 0755 /home/user || true && \
    chown -R 1000:1000 /home/user || true

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Help text from %runscript
# Apptainer image for the symlink staging configuration task.
# Start an interactive shell with: apptainer exec $0 /bin/bash