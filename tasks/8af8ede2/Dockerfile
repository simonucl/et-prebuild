FROM ubuntu:22.04

# Help text
# This container image provides the starting environment for the
# log-filtering assignment. It contains:
#   - /home/user/logs/access.log (fixture input log)
#   - Python 3 and pytest (for automated grading)
# The writable permissions on /home/user allow an unprivileged user
# to create the required output files during the exercise.

LABEL Author="AI Assistant"
LABEL Description="Environment for log-filtering exercise with pytest installed."

ENV DEBIAN_FRONTEND=noninteractive

RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/logs

RUN cat > /home/user/logs/access.log << 'EOF'
127.0.0.1 - - [15/Sep/2023:10:15:30 +0000] "GET /api/login HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
192.168.1.10 - - [15/Sep/2023:11:02:15 +0000] "POST /api/purchase HTTP/1.1" 503 542 "-" "curl/7.68.0"
10.0.0.3 - - [15/Sep/2023:11:45:50 +0000] "GET /dashboard HTTP/1.1" 500 654 "-" "Mozilla/5.0"
127.0.0.1 - - [14/Sep/2023:09:01:12 +0000] "GET /index.html HTTP/1.1" 404 102 "-" "Mozilla/5.0"
192.168.1.11 - - [15/Sep/2023:12:00:00 +0000] "POST /api/upload HTTP/1.1" 201 1024 "-" "curl/7.68.0"
10.0.0.4 - - [15/Sep/2023:12:30:25 +0000] "GET /status HTTP/1.1" 502 210 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Sep/2023:12:32:01 +0000] "GET /api/data HTTP/1.1" 200 321 "-" "Mozilla/5.0"
192.168.1.12 - - [16/Sep/2023:00:10:05 +0000] "GET /maintenance HTTP/1.1" 503 333 "-" "curl/7.68.0"
10.0.0.5 - - [15/Sep/2023:13:15:45 +0000] "POST /api/logout HTTP/1.1" 500 400 "-" "Mozilla/5.0"
127.0.0.1 - - [15/Sep/2023:14:55:10 +0000] "GET /nonexistent HTTP/1.1" 404 98 "-" "Mozilla/5.0"
EOF

RUN chmod -R 0777 /home/user && chown -R 0:0 /home/user