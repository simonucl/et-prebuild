# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author label
LABEL Author="Automated build for log-analysis task"

# Install Python 3, pip and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-privileged user `user`
RUN useradd -m -s /bin/bash user

# Set up initial directory structure and access log
RUN LOG_DIR="/home/user/logs" && \
    mkdir -p "${LOG_DIR}"

RUN cat > "/home/user/logs/webserver_access.log" <<'EOF'
203.0.113.1 - - [15/Feb/2023:08:57:03 +0000] "GET /index.html HTTP/1.1" 200 1024
198.51.100.2 - - [15/Feb/2023:09:10:44 +0000] "GET /about HTTP/1.1" 200 850
192.0.2.3 - - [14/Feb/2023:23:59:59 +0000] "GET / HTTP/1.1" 200 600
203.0.113.1 - - [15/Feb/2023:09:12:15 +0000] "POST /login HTTP/1.1" 302 517
198.51.100.2 - - [15/Feb/2023:09:13:47 +0000] "GET /dashboard HTTP/1.1" 200 2048
203.0.113.1 - - [15/Feb/2023:09:14:23 +0000] "GET /index.html HTTP/1.1" 200 1024
203.0.113.1 - - [15/Feb/2023:09:20:55 +0000] "GET /products HTTP/1.1" 200 4096
192.0.2.3 - - [15/Feb/2023:09:22:07 +0000] "GET /contact HTTP/1.1" 404 256
198.51.100.2 - - [15/Feb/2023:09:30:18 +0000] "GET /pricing HTTP/1.1" 200 1536
203.0.113.5 - - [16/Feb/2023:07:00:01 +0000] "GET /old-page HTTP/1.1" 301 245
203.0.113.1 - - [15/Feb/2023:10:01:33 +0000] "GET /blog HTTP/1.1" 200 11200
198.51.100.9 - - [15/Feb/2023:11:22:10 +0000] "GET /random HTTP/1.1" 200 100
203.0.113.7 - - [13/Feb/2023:17:45:22 +0000] "GET /archive HTTP/1.1" 200 640
192.0.2.3 - - [15/Feb/2023:12:00:00 +0000] "GET /contact HTTP/1.1" 404 256
203.0.113.1 - - [15/Feb/2023:12:15:45 +0000] "GET /cart HTTP/1.1" 200 768
EOF

# Ensure regular permissions and ownership
RUN chown -R user:user /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Default command
CMD ["/bin/bash"]