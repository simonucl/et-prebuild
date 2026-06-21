# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python, pip, and dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        gnupg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Prepare filesystem
RUN mkdir -p /home/user && \
    mkdir -p /home/user/mobile_build/config && \
    mkdir -p /home/user/mobile_build/logs && \
    chmod 700 /home/user/mobile_build && \
    chmod 700 /home/user/mobile_build/config && \
    chmod 700 /home/user/mobile_build/logs

# Create INI file
RUN cat <<'EOF' > /home/user/mobile_build/config/app_build.ini
[build]
build_flavor=production
min_sdk=21
target_sdk=34

[version]
version_name=2.3.5
version_code=235
EOF

# Set permissions on INI file
RUN chmod 600 /home/user/mobile_build/config/app_build.ini

# Environment setup
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Fix home directory permissions
RUN chmod 755 /home/user

# Labels
LABEL Author="android_build_prep_example"