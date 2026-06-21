# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="automated" \
      Description="Base image for configuration-patching task with pytest pre-installed."

# ------------------------------------------------------------------
# Install Python and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Create home directory and initial repository structure
# ------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user/projects/deploy && \
    chmod 700 /home/user/projects/deploy

# ------------------ config.yaml (baseline) ------------------------
RUN cat > /home/user/projects/deploy/config.yaml << 'EOF'
app:
  name: "AcmeApp"
  version: "1.2.3"
  env: "staging"

services:
  auth:
    enabled: true
    port: 8080
  api:
    enabled: true
    port: 9000
EOF

# ------------------ settings.toml (baseline) ----------------------
RUN cat > /home/user/projects/deploy/settings.toml << 'EOF'
[general]
owner = "devops team"
timeout = 30

[features]
logging = true
metrics = false
EOF

# Ensure the required permissions
RUN set -e && \
    chmod 644 /home/user/projects/deploy/config.yaml && \
    chmod 644 /home/user/projects/deploy/settings.toml && \
    chmod 755 /home/user

# ------------------------------------------------------------------
# Environment variables (from %environment)
# ------------------------------------------------------------------
ENV LC_ALL=C.UTF-8 \
    PYTHONIOENCODING=utf-8

# ------------------------------------------------------------------
# Help (from %help)
# ------------------------------------------------------------------
# This container sets up the initial state for the "configuration patching" task.
#
# It provides:
#   • /home/user/projects/deploy/config.yaml   (baseline)
#   • /home/user/projects/deploy/settings.toml (baseline)
#
# pytest is pre-installed so the automated grader can run its test suite.