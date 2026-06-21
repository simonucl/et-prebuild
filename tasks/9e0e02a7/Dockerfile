# Converted from Apptainer definition file
FROM ubuntu:22.04

# Install packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        git \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN python3 -m pip install --no-cache-dir pytest

# Prepare initial repository
RUN mkdir -p /home/user/edge-devices && \
    cd /home/user/edge-devices && \
    git init -b main && \
    git config --system user.name "Apptainer Builder" && \
    git config --system user.email "builder@example.com" && \
    echo "0.9.4" > VERSION

# Create CHANGELOG.md via heredoc
RUN cat > /home/user/edge-devices/CHANGELOG.md <<'EOF'
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.9.4] – 2023-10-07
- Added support for dynamic topic subscriptions.

## [0.9.3] – 2023-09-12
- Improved TLS handshake performance.

EOF

# Stage and commit initial files
RUN cd /home/user/edge-devices && \
    git add VERSION CHANGELOG.md && \
    git commit -m "feat: initial state 0.9.4" && \
    chmod -R a+rwX /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8