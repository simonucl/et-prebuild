# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help / labels
LABEL Author="ChatGPT"
LABEL Description="Starter container for the Nginx-log regex extraction task. Includes pytest and the required legacy log files."

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Post section
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user || true

RUN mkdir -p /home/user/project/logs

RUN echo '# placeholder log for 14 Aug 2023' > /home/user/project/logs/2023-08-14_access.log

RUN cat > /home/user/project/logs/2023-08-15_access.log <<'EOF'
192.168.1.10 - - [15/Aug/2023:10:15:32 +0000] "GET /index.html HTTP/1.1" 200 5320 "-" "Mozilla/5.0"
192.168.1.11 - - [15/Aug/2023:10:16:02 +0000] "POST /api/v1/login HTTP/1.1" 401 298 "-" "curl/7.68.0"
192.168.1.12 - - [15/Aug/2023:10:17:45 +0000] "GET /dashboard HTTP/1.1" 500 1032 "-" "Mozilla/5.0"
192.168.1.13 - - [15/Aug/2023:10:18:01 +0000] "GET /favicon.ico HTTP/1.1" 200 543 "-" "Mozilla/5.0"
192.168.1.14 - - [15/Aug/2023:10:19:27 +0000] "GET /api/v1/data HTTP/1.1" 200 2780 "-" "Mozilla/5.0"
192.168.1.15 - - [15/Aug/2023:10:20:14 +0000] "POST /api/v1/update HTTP/1.1" 503 64 "-" "Python-urllib/3.8"
192.168.1.16 - - [15/Aug/2023:10:21:05 +0000] "GET /hidden HTTP/1.1" 403 232 "-" "curl/7.68.0"
192.168.1.17 - - [15/Aug/2023:10:22:47 +0000] "DELETE /api/v1/data HTTP/1.1" 200 34 "-" "Mozilla/5.0"
192.168.1.18 - - [15/Aug/2023:10:23:55 +0000] "GET /status HTTP/1.1" 200 123 "-" "Mozilla/5.0"
192.168.1.19 - - [15/Aug/2023:10:24:30 +0000] "GET /report HTTP/1.1" 512 67 "-" "Mozilla/5.0"
192.168.1.20 - - [15/Aug/2023:10:25:11 +0000] "GET /index.html HTTP/1.1" 304 0 "-" "Mozilla/5.0"
192.168.1.21 - - [15/Aug/2023:10:26:07 +0000] "GET /unknown HTTP/1.1" 404 88 "-" "Mozilla/5.0"
EOF

RUN chmod -R 0777 /home/user/project

RUN chmod 755 /home/user