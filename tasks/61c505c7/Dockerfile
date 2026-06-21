FROM ubuntu:22.04

# Labels
LABEL Author="Automatic build for Nginx access-log reporting kata"
LABEL Description="Base container with raw log and pytest ready for student exercises"

# Environment variables
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV PYTHONIOENCODING=utf-8

# System packages and Python tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        locales && \
    rm -rf /var/lib/apt/lists/* && \
    sed -i 's/^# *\(en_US.UTF-8 UTF-8\)/\1/' /etc/locale.gen && \
    locale-gen && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Create expected directory layout
RUN mkdir -p /home/user/projects/website/logs /home/user/projects/website/reports && \
    chmod 0777 /home/user/projects/website/reports

# Write the pre-existing access log
RUN cat <<'EOF' > /home/user/projects/website/logs/access.log
127.0.0.1 - - [15/Aug/2023:09:00:01 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:09:02:17 +0000] "GET /style.css HTTP/1.1" 200 2048 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:09:05:59 +0000] "GET /script.js HTTP/1.1" 200 4096 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:14:01:14 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:14:05:23 +0000] "GET /api/data HTTP/1.1" 200 512 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:14:10:45 +0000] "GET /old-page HTTP/1.1" 301 0 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:14:15:33 +0000] "GET /favicon.ico HTTP/1.1" 404 0 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:15:00:12 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:15:02:02 +0000] "GET /api/data HTTP/1.1" 200 512 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:15:04:31 +0000] "GET /login HTTP/1.1" 200 256 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:15:05:45 +0000] "GET /about.html HTTP/1.1" 200 2048 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:15:06:55 +0000] "GET /server-error HTTP/1.1" 500 0 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:15:08:22 +0000] "GET /api/data HTTP/1.1" 500 0 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:15:09:23 +0000] "GET /login HTTP/1.1" 302 0 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:16:01:05 +0000] "GET /favicon.ico HTTP/1.1" 404 0 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:16:02:45 +0000] "GET /about.html HTTP/1.1" 200 2048 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:15:11:11 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:15:12:22 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:15:13:33 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:15:14:44 +0000] "GET /login HTTP/1.1" 200 256 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:15:16:55 +0000] "GET /login HTTP/1.1" 200 256 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:15:18:08 +0000] "GET /api/data HTTP/1.1" 200 512 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:15:19:19 +0000] "GET /api/data HTTP/1.1" 200 512 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:14:20:55 +0000] "GET /about.html HTTP/1.1" 200 2048 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Aug/2023:15:21:21 +0000] "GET /favicon.ico HTTP/1.1" 404 0 "-" "Mozilla/5.0"
EOF

RUN chmod 0644 /home/user/projects/website/logs/access.log && \
    chmod 755 /home/user

WORKDIR /home/user

# Help information (as comments):
# This container image provides the starting environment for the
# "Nginx access-log reporting" exercise.
#
# • Python 3 and pytest are installed.
# • The raw access log is located at:
#       /home/user/projects/website/logs/access.log
# • The reports directory is present and empty (writable) at:
#       /home/user/projects/website/reports
#
# All other task requirements must be fulfilled by the student.