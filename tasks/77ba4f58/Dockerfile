# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update package lists and install required packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        iputils-ping \
        fping \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading harness
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Set up the initial filesystem state for the exercise
RUN mkdir -p /home/user && \
    chmod 777 /home/user

RUN cat >/home/user/services.list <<'EOF'
127.0.0.1
192.0.2.1
203.0.113.1
EOF

RUN chmod 644 /home/user/services.list

# Ensure correct permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8