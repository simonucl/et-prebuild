# syntax=docker/dockerfile:1
# Converted from Apptainer definition file
FROM ubuntu:22.04

# System packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create application user and home
RUN useradd -m -u 1000 -s /bin/bash user

# Prepare mock-service directory structure and JSON files
RUN mkdir -p /home/user/mock_services && \
    printf '{"status":"ok","service":"auth"}\n' > /home/user/mock_services/auth.json && \
    printf '{"status":"ok","service":"user"}\n' > /home/user/mock_services/user.json && \
    printf '{"status":"ok","service":"payment"}\n' > /home/user/mock_services/payment.json

# Permissions
RUN chmod 0755 /home/user/mock_services && \
    chmod 0644 /home/user/mock_services/*.json && \
    chmod 0777 /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Help text
# Placeholder section required by some build systems; intentionally left empty.