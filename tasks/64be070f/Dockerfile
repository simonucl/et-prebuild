# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Minimal locale settings for predictable tool behaviour
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Basic utilities and Python tooling
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        dnsutils \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test harness
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare initial filesystem layout for the exercise
# ------------------------------------------------------------------

# Ensure /home/user hierarchy exists
RUN mkdir -p /home/user

# 1. /home/user/data directory and CSV file
RUN mkdir -p /home/user/data && \
    chmod 755 /home/user/data

RUN cat > /home/user/data/domains.csv <<'EOF'
domain
example.com
iana.org
EOF

RUN chmod 644 /home/user/data/domains.csv

# 2. /home/user/output directory (initially empty)
RUN mkdir -p /home/user/output && \
    chmod 755 /home/user/output

# Default container command (from %runscript)
CMD echo "Container for the 'domain -> IPv4' resolution task." && \
    echo "Use standard Linux tools inside the container to complete the exercise."