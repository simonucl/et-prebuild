# syntax=docker/dockerfile:1
# Using ubuntu:22.04 as base image
FROM ubuntu:22.04

# Basic tooling
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create initial project structure
RUN mkdir -p /home/user/project

# VERSION file
RUN printf '1.4.2\n' > /home/user/project/VERSION

# CHANGELOG.md with heredoc
RUN cat > /home/user/project/CHANGELOG.md <<'EOF'
# Changelog
All notable changes to this project will be documented in this file.

## [1.4.2] - 2023-12-14
### Changed
* Switched default output from JSON to YAML.
EOF

# Permissions
RUN chmod -R 777 /home/user/project && chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8