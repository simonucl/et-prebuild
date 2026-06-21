# syntax=docker/dockerfile:1
FROM ubuntu:22.04

LABEL Author="Agent-Prep" \
      Description="Environment for Docker-command audit exercise. Provides Python, pytest, and a stub ‘docker’ CLI."

# ------------------------------------------------------------------
# Basic build tools and Python stack
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Make sure /usr/local/bin is on the default PATH
RUN mkdir -p /usr/local/bin

# ------------------------------------------------------------------
# Stub implementation of the Docker CLI
# ------------------------------------------------------------------
RUN cat <<'EOF' > /usr/local/bin/docker
#!/usr/bin/env bash
# ------------------------------------------------------------
# Minimal stub for the Docker CLI used in the training sandbox.
# It simply echoes the command it was asked to run and exits 0
# so that learners can capture a successful exit status.
# ------------------------------------------------------------
echo "Simulated docker command: $*" >&2
exit 0
EOF

RUN chmod 0755 /usr/local/bin/docker

# ------------------------------------------------------------------
# Create the /home/user directory (ownership root:root)
# ------------------------------------------------------------------
RUN mkdir -p /home/user && \
    chmod 755 /home/user

# ------------------------------------------------------------------
# Clean up APT caches to keep the image slim
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Environment variables
# ------------------------------------------------------------------
ENV PATH=/usr/local/bin:$PATH

# ------------------------------------------------------------------
# Help
# ------------------------------------------------------------------
# This image contains:
#   • Python 3 + pytest (for automated grading)
#   • A stub ‘docker’ command that always succeeds (exit status 0)
#
# The exercise instructions will guide you through running three
# specific Docker commands and writing an audit log at:
#     /home/user/activities/analytics-pg_optimize_commands.log
#
# The log file should NOT exist when the container is first started.