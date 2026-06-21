# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Maintainer label from Apptainer %labels
LABEL Maintainer="CI Prototype Container"

# %help
# This container provides the initial filesystem state and tooling
# (including pytest) required for the CI prototype automation task.

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

# Prepare initial project state
RUN set -e && \
    mkdir -p /home/user/projects/ci && \
    cat > /home/user/projects/ci/pipeline.yml <<'EOF'
version: "1.0"
jobs:
  build:
    steps:
      - run: echo "Building"
EOF

# Permissions
RUN set -e && \
    chmod 644 /home/user/projects/ci/pipeline.yml && \
    chmod 755 /home/user && \
    chmod 755 /home/user/projects && \
    chmod 755 /home/user/projects/ci