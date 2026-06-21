# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python tooling for the grader
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# Ensure /home/user is writable
RUN mkdir -p /home/user && chmod 777 /home/user

# Create project directory
RUN mkdir -p /home/user/projects/test_env

RUN cat > /home/user/projects/test_env/config.yaml << 'EOF'
env: staging
version: 1.0
EOF

RUN cat > /home/user/projects/test_env/test_data.csv << 'EOF'
id,value
1,foo
2,bar
EOF

RUN cat > /home/user/projects/test_env/readme.md << 'EOF'
# Test Environment
This directory contains configuration and data for QA tests.
EOF

# Fix permissions
RUN chmod -R a+rwX /home/user/projects

# Environment setup
RUN chmod 755 /home/user
ENV PATH="$PATH:/usr/local/bin"

LABEL Author="QA-Apptainer-Setup"
LABEL Description="Environment for backup/archiving exercise with pytest pre-installed"

# This container provides the initial state for the backup task.
# Source files live under /home/user/projects/test_env and pytest is available for automated grading.