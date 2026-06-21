# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python tooling
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state
RUN mkdir -p /home/user/sys-hardening

# VERSION file
RUN printf '2.1.9\n' > /home/user/sys-hardening/VERSION

# CHANGELOG.md (heredoc)
RUN cat <<'EOF' > /home/user/sys-hardening/CHANGELOG.md
# Change Log
All notable changes to this project will be documented in this file.

## [Unreleased]
### Added
- Implemented new SSL cipher suites.
- Added automated backup rotation.

### Fixed
- Corrected typo in Nginx worker_connections directive.
EOF

# Ensure non-root users can read the repository files
RUN chmod -R a+rX /home/user/sys-hardening

# Ensure home directory has correct permissions
RUN chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH