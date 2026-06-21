FROM ubuntu:22.04

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    chmod 755 /home/user

RUN mkdir -p /home/user/logs && \
    cat >/home/user/logs/access.log <<'EOF'
127.0.0.1 - - [12/May/2023:06:25:24 +0000] "GET /index.html HTTP/1.1" 200 1024
127.0.0.1 - - [12/May/2023:06:25:25 +0000] "GET /favicon.ico HTTP/1.1" 404 209
192.168.0.5 - - [12/May/2023:06:25:26 +0000] "GET /missing.png HTTP/1.1" 404 512
10.0.0.1 - - [12/May/2023:06:25:27 +0000] "POST /login HTTP/1.1" 200 2048
10.0.0.2 - - [12/May/2023:06:25:28 +0000] "GET /dashboard HTTP/1.1" 301 342
172.16.0.3 - - [12/May/2023:06:25:29 +0000] "GET /secret HTTP/1.1" 403 128
127.0.0.1 - - [12/May/2023:06:25:30 +0000] "GET /robots.txt HTTP/1.1" 200 67
192.168.0.5 - - [12/May/2023:06:25:31 +0000] "GET /notfound.html HTTP/1.1" 404 256
10.0.0.1 - - [12/May/2023:06:25:32 +0000] "GET /index.html HTTP/1.1" 200 1024
10.0.0.2 - - [12/May/2023:06:25:33 +0000] "GET /contact HTTP/1.1" 200 512
EOF

RUN chmod 644 /home/user/logs/access.log

# Container for Apache log monitoring task.