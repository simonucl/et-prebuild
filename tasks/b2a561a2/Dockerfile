# syntax=docker/dockerfile:1
# Converted from Apptainer definition
FROM ubuntu:22.04

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# System packages and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eu && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Directory structure and permissions
RUN mkdir -p /home/user/logs/webserver && \
    mkdir -p /home/user/reports && \
    chmod 755 /home && \
    chmod 755 /home/user && \
    chmod 755 /home/user/logs && \
    chmod 755 /home/user/logs/webserver && \
    chmod 777 /home/user/reports

# Seed access.log
RUN cat > /home/user/logs/webserver/access.log <<'EOF'
192.168.0.10 - - [10/Jan/2023:08:15:01 +0000] "GET /index.html HTTP/1.1" 200 612
54.23.12.1 - - [10/Jan/2023:08:15:05 +0000] "POST /api/login HTTP/1.1" 200 1420
203.0.113.55 - - [10/Jan/2023:08:16:13 +0000] "GET /admin HTTP/1.1" 403 721
198.51.100.23 - - [10/Jan/2023:08:17:42 +0000] "GET /images/logo.png HTTP/1.1" 200 2048
192.0.2.44 - - [10/Jan/2023:08:18:09 +0000] "GET /admin/settings HTTP/1.1" 404 512
203.0.113.55 - - [10/Jan/2023:08:18:57 +0000] "GET /dashboard HTTP/1.1" 500 890
54.23.12.1 - - [10/Jan/2023:08:19:31 +0000] "GET /api/data HTTP/1.1" 503 112
198.51.100.23 - - [10/Jan/2023:08:20:15 +0000] "GET /contact.html HTTP/1.1" 200 430
192.0.2.44 - - [10/Jan/2023:08:20:45 +0000] "GET /admin HTTP/1.1" 401 512
203.0.113.55 - - [10/Jan/2023:08:21:10 +0000] "POST /api/upload HTTP/1.1" 201 1340
EOF

RUN chmod 644 /home/user/logs/webserver/access.log

# Labels
LABEL Author="devsecops-preparer"
LABEL Description="Initial state for policy-as-code assignment"