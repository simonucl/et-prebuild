# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer %labels
LABEL Author="Your Name" \
      Description="Apptainer image for CI/CD INI parsing task with pytest pre-installed."

# ------------------------------------------------------------------------------
# Install Python and pytest
# ------------------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------------------
# Set up initial filesystem state required for the exercise
# ------------------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user/cicd && \
    chmod 0777 /home/user/cicd

# Create the pristine pipeline.ini with the exact expected contents
RUN cat > /home/user/cicd/pipeline.ini << 'EOF'
[metadata]
project_name = Nebula
build_number = 42

[deploy]
envs = dev,staging,prod
strategy = rolling

[notifications]
slack = true
email = false
EOF

# Ensure sensible permissions
RUN chmod 0644 /home/user/cicd/pipeline.ini

# ------------------------------------------------------------------------------
# Environment setup (from %environment)
# ------------------------------------------------------------------------------
RUN chmod 755 /home/user

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# ------------------------------------------------------------------------------
# Help (from %help)
# This image is intended for a CI/CD INI parsing task with pytest pre-installed.
# ------------------------------------------------------------------------------