# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# %help
# Container pre-configured for the “patch-release” exercise.
# Includes:
#  • Git repository at /home/user/projects/acme-service (version 2.4.1)
#  • Python3 + pytest
#  • All files world-writable so an unprivileged user can complete the task.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        git \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN set -e && \
    mkdir -p /home/user/projects/acme-service

RUN cat > /home/user/projects/acme-service/VERSION <<'EOF'
2.4.1
EOF

RUN cat > /home/user/projects/acme-service/CHANGELOG.md <<'EOF'
# Changelog

All notable changes to this project will be documented in this file.

## [2.4.1] - 2023-06-15
- Fixed authentication middleware race condition (#342)

## [2.4.0] - 2023-05-28
- Added OAuth2 support (#315)
EOF

RUN set -e && \
    cd /home/user/projects/acme-service && \
    git init -b main && \
    git config user.email "builder@example.com" && \
    git config user.name "Builder" && \
    git add VERSION CHANGELOG.md && \
    git commit -m "Initial commit"

RUN chmod -R a+rwX /home/user

# %labels
# Author: Apptainer build script for ACME service patch-release exercise
# Note: Original Apptainer labels section contained a chmod directive; permissions are handled above.