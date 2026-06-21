# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Prepare initial filesystem state for the log-analysis task
# ------------------------------------------------------------------
# Create the required directory tree
RUN mkdir -p /home/user/webapp/logs

# Populate access.log with the canonical contents
RUN cat > /home/user/webapp/logs/access.log <<'EOF'
127.0.0.1 - - [12/Jun/2023:10:55:32 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
192.168.0.42 - - [12/Jun/2023:10:55:35 +0000] "GET /does-not-exist HTTP/1.1" 404 512 "-" "Mozilla/5.0"
10.10.10.10 - - [12/Jun/2023:10:55:37 +0000] "POST /login HTTP/1.1" 302 256 "-" "Mozilla/5.0"
172.16.0.5 - - [12/Jun/2023:10:55:40 +0000] "GET /admin HTTP/1.1" 403 2048 "-" "Mozilla/5.0"
192.168.0.42 - - [12/Jun/2023:10:55:45 +0000] "GET /another-missing HTTP/1.1" 404 512 "-" "Mozilla/5.0"
203.0.113.77 - - [12/Jun/2023:10:55:50 +0000] "GET /favicon.ico HTTP/1.1" 404 128 "-" "Mozilla/5.0"
127.0.0.1 - - [12/Jun/2023:10:56:01 +0000] "GET /assets/css/main.css HTTP/1.1" 200 4096 "-" "Mozilla/5.0"
EOF

# Ensure correct permissions on the log file and home directory
RUN chmod 0644 /home/user/webapp/logs/access.log && \
    chmod 755 /home/user

# ------------------------------------------------------------------
# Environment configuration
# ------------------------------------------------------------------
ENV PYTHONIOENCODING="utf-8"

# ------------------------------------------------------------------
# Labels
# ------------------------------------------------------------------
LABEL Author="Task preparation: Apache 404 log-analysis" \
      Description="Container with initial state for students to extract 404 IP addresses using awk/sed."