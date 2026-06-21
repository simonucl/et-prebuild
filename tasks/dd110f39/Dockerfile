FROM ubuntu:22.04

# Update package lists and install system packages
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        nodejs \
        npm \
        git \
        ca-certificates

# Install Python dependencies
RUN pip3 install --no-cache-dir pytest

# Install markdownlint CLI globally
RUN npm install -g markdownlint-cli

# Create the initial sample repository expected by the assignment
RUN mkdir -p /home/user/project/config

# app.conf
RUN cat > /home/user/project/config/app.conf <<'EOF'
# Application configuration
ENABLE_FEATURE_X=false
LOG_LEVEL=info
EOF

# db.conf
RUN cat > /home/user/project/config/db.conf <<'EOF'
# Database configuration
max_connections=100
shared_buffers=128MB
EOF

# README.md (content not strictly validated)
RUN cat > /home/user/project/README.md <<'EOF'
# Sample Project

This is a placeholder README for the configuration-manager exercise.
EOF

# Ensure the student (non-root) can write into /home/user/**
RUN chmod -R a+rwX /home/user

# Environment variables
ENV PATH="/usr/local/bin:$PATH"

# Set permissions on startup
RUN chmod 755 /home/user