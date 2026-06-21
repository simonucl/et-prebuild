FROM ubuntu:22.04

LABEL Author="TaskSetup"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip tzdata ca-certificates \
        coreutils gawk grep sed && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/logs

RUN cat > /home/user/logs/access.log <<'EOF'
127.0.0.1 - - [12/Mar/2024:10:15:32 +0000] "GET /index.html HTTP/1.1" 200 512 "-" "Mozilla/5.0"
192.168.1.10 - - [12/Mar/2024:10:20:05 +0000] "POST /login HTTP/1.1" 302 1234 "-" "Mozilla/5.0"
203.0.113.5 - - [12/Mar/2024:11:05:44 +0000] "GET /products HTTP/1.1" 200 2048 "-" "Mozilla/5.0"
192.168.1.10 - - [12/Mar/2024:11:18:10 +0000] "GET /dashboard HTTP/1.1" 200 4096 "-" "Mozilla/5.0"
198.51.100.23 - - [12/Mar/2024:12:01:01 +0000] "GET /index.html HTTP/1.1" 200 512 "-" "Mozilla/5.0"
192.168.1.10 - - [12/Mar/2024:12:35:47 +0000] "GET /profile HTTP/1.1" 200 8192 "-" "Mozilla/5.0"
203.0.113.5 - - [12/Mar/2024:12:45:00 +0000] "GET /cart HTTP/1.1" 404 256 "-" "Mozilla/5.0"
203.0.113.5 - - [12/Mar/2024:12:46:10 +0000] "POST /checkout HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
203.0.113.5 - - [12/Mar/2024:12:47:22 +0000] "GET /thanks HTTP/1.1" 200 512 "-" "Mozilla/5.0"
198.51.100.23 - - [12/Mar/2024:13:00:00 +0000] "GET /blog HTTP/1.1" 200 512 "-" "Mozilla/5.0"
198.51.100.23 - - [12/Mar/2024:13:05:30 +0000] "GET /blog/post1 HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
192.168.1.10 - - [12/Mar/2024:14:10:10 +0000] "GET /logout HTTP/1.1" 200 256 "-" "Mozilla/5.0"
EOF

RUN chmod 755 /home/user/logs && \
    chmod 644 /home/user/logs/access.log && \
    chmod 777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/local/bin:${PATH}"

WORKDIR /home/user