# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text
# This image sets up the initial state for the "SecOps log analysis" task.
# - Apache combined log located at /home/user/logs/webapp_access.log
# - No analysis artefacts present.
# - pytest installed system-wide for automated grading.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip gawk sed && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

RUN mkdir -p /home/user/logs

RUN cat > /home/user/logs/webapp_access.log <<'EOF'
192.168.1.10 - - [15/Apr/2024:10:01:01 -0700] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
192.168.1.10 - - [15/Apr/2024:10:02:15 -0700] "POST /login HTTP/1.1" 200 2048 "-" "Mozilla/5.0"
192.168.1.10 - - [15/Apr/2024:10:03:22 -0700] "GET /dashboard HTTP/1.1" 200 4096 "-" "Mozilla/5.0"
192.168.1.10 - - [15/Apr/2024:10:04:05 -0700] "GET /settings HTTP/1.1" 200 2048 "-" "Mozilla/5.0"
192.168.1.10 - - [15/Apr/2024:10:05:47 -0700] "GET /profile HTTP/1.1" 200 3072 "-" "Mozilla/5.0"
192.168.1.10 - - [15/Apr/2024:10:06:30 -0700] "GET /notfound HTTP/1.1" 404 512 "-" "Mozilla/5.0"
192.168.1.10 - - [15/Apr/2024:10:07:12 -0700] "GET /server-error HTTP/1.1" 500 256 "-" "Mozilla/5.0"
10.0.0.2 - - [15/Apr/2024:11:00:10 -0700] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
10.0.0.2 - - [15/Apr/2024:11:01:24 -0700] "GET /catalog HTTP/1.1" 200 2048 "-" "Mozilla/5.0"
10.0.0.2 - - [15/Apr/2024:11:02:55 -0700] "GET /cart HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
10.0.0.2 - - [15/Apr/2024:11:03:40 -0700] "GET /checkout HTTP/1.1" 200 2048 "-" "Mozilla/5.0"
10.0.0.2 - - [15/Apr/2024:11:04:18 -0700] "GET /missing HTTP/1.1" 404 512 "-" "Mozilla/5.0"
172.16.0.3 - - [15/Apr/2024:12:00:05 -0700] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
172.16.0.3 - - [15/Apr/2024:12:01:37 -0700] "GET /blog HTTP/1.1" 200 4096 "-" "Mozilla/5.0"
172.16.0.3 - - [15/Apr/2024:12:02:42 -0700] "GET /contact HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
172.16.0.3 - - [15/Apr/2024:12:03:59 -0700] "GET /old-page HTTP/1.1" 404 512 "-" "Mozilla/5.0"
203.0.113.55 - - [15/Apr/2024:13:00:10 -0700] "GET /error HTTP/1.1" 500 256 "-" "Mozilla/5.0"
198.51.100.23 - - [15/Apr/2024:13:02:23 -0700] "GET /api/bad HTTP/1.1" 500 256 "-" "Mozilla/5.0"
192.0.2.44 - - [15/Apr/2024:13:04:34 -0700] "GET /fail HTTP/1.1" 500 256 "-" "Mozilla/5.0"
203.0.113.55 - - [15/Apr/2024:13:05:45 -0700] "GET /unknown HTTP/1.1" 404 512 "-" "Mozilla/5.0"
198.51.100.23 - - [15/Apr/2024:13:06:56 -0700] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
192.0.2.44 - - [15/Apr/2024:13:08:07 -0700] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
198.51.100.23 - - [15/Apr/2024:13:09:18 -0700] "GET /notfound HTTP/1.1" 404 512 "-" "Mozilla/5.0"
203.0.113.55 - - [15/Apr/2024:13:10:29 -0700] "GET /contact HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
192.0.2.44 - - [15/Apr/2024:13:11:40 -0700] "GET /about HTTP/1.1" 404 512 "-" "Mozilla/5.0"
EOF

RUN chmod -R 0777 /home/user

ENV HOME=/home/user