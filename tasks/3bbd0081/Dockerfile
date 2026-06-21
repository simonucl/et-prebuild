FROM ubuntu:22.04

# Author: devops-ai
# Description: Container set-up for HTTP status-code frequency task

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/logs && \
    mkdir -p /home/user/output && \
    chmod 755 /home/user && \
    chmod 755 /home/user/logs && \
    chmod 755 /home/user/output && \
    rm -rf /var/lib/apt/lists/*

RUN cat > /home/user/logs/access.log <<'EOF'
127.0.0.1 - - [01/Jan/2023:10:00:00 +0000] "GET /index.html HTTP/1.1" 200 1024
192.168.0.10 - - [01/Jan/2023:10:00:01 +0000] "GET /about HTTP/1.1" 200 512
10.0.0.5 - - [01/Jan/2023:10:00:02 +0000] "POST /login HTTP/1.1" 401 256
127.0.0.1 - - [01/Jan/2023:10:00:03 +0000] "GET /doesnotexist HTTP/1.1" 404 128
127.0.0.1 - - [01/Jan/2023:10:00:04 +0000] "GET /index.html HTTP/1.1" 200 1024
10.0.0.5 - - [01/Jan/2023:10:00:05 +0000] "POST /login HTTP/1.1" 401 256
192.168.0.10 - - [01/Jan/2023:10:00:06 +0000] "GET /contact HTTP/1.1" 200 512
192.168.0.11 - - [01/Jan/2023:10:00:07 +0000] "GET /index.html HTTP/1.1" 500 128
127.0.0.1 - - [01/Jan/2023:10:00:08 +0000] "GET /index.html HTTP/1.1" 200 1024
192.168.0.11 - - [01/Jan/2023:10:00:09 +0000] "GET /index.html HTTP/1.1" 500 128
10.0.0.5 - - [01/Jan/2023:10:00:10 +0000] "POST /login HTTP/1.1" 401 256
192.168.0.10 - - [01/Jan/2023:10:00:11 +0000] "GET /about HTTP/1.1" 200 512
EOF

RUN chmod 644 /home/user/logs/access.log