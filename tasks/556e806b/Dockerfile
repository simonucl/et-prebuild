# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------
# Basic tools and Python + pytest
# ------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest via pip to ensure a recent version
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------
# Create initial filesystem state for the student.
# ------------------------------------------------------------
# Create user and home directory (even though tests run as the caller)
RUN set -e && \
    if ! id -u user >/dev/null 2>&1; then \
        useradd -m -d /home/user -s /bin/bash user; \
    fi

# Directory for logs
RUN mkdir -p /home/user/logs && \
    chmod 755 /home/user/logs

# Pre-populated webserver.log with exact, required contents
RUN cat >/home/user/logs/webserver.log <<'EOF'
127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 1024
192.168.1.10 - - [10/Oct/2023:14:01:02 +0000] "GET /not-found HTTP/1.1" 404 512
203.0.113.5 - - [10/Oct/2023:14:03:17 +0000] "POST /login HTTP/1.1" 302 214
198.51.100.23 - - [10/Oct/2023:14:06:44 +0000] "GET /old-page HTTP/1.1" 404 198
192.0.2.77 - - [10/Oct/2023:14:09:58 +0000] "GET /favicon.ico HTTP/1.1" 200 543
192.168.1.10 - - [10/Oct/2023:14:12:11 +0000] "GET /robots.txt HTTP/1.1" 404 87
203.0.113.5 - - [10/Oct/2023:14:14:29 +0000] "GET /missing.jpg HTTP/1.1" 404 64
198.51.100.23 - - [10/Oct/2023:14:17:03 +0000] "GET /archive.zip HTTP/1.1" 200 3245
192.0.2.77 - - [10/Oct/2023:14:19:43 +0000] "HEAD /secret HTTP/1.1" 404 0
127.0.0.1 - - [10/Oct/2023:14:22:55 +0000] "GET /index.html HTTP/1.1" 200 1024
EOF

RUN chmod 644 /home/user/logs/webserver.log && \
    chmod 755 /home/user

# ------------------------------------------------------------
# Environment
# ------------------------------------------------------------
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# ------------------------------------------------------------
# Labels
# ------------------------------------------------------------
LABEL Author="Apptainer build script for log analysis task" \
      Description="Container providing initial state and pytest for automated grading"

# ------------------------------------------------------------
# Default command (equivalent to empty runscript)
# ------------------------------------------------------------
CMD ["bash"]