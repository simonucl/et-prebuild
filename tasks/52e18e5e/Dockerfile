FROM ubuntu:22.04

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user
RUN mkdir -p /home/user/server_logs

RUN cat > /home/user/server_logs/access.log << 'EOF'
192.168.0.1 - - [12/Jun/2023:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 1024
192.168.0.1 - - [12/Jun/2023:10:01:35 +0000] "POST /login HTTP/1.1" 302 512
10.0.0.5 - - [12/Jun/2023:10:02:10 +0000] "GET /about.html HTTP/1.1" 200 2048
203.0.113.10 - - [12/Jun/2023:10:03:22 +0000] "GET /contact.html HTTP/1.1" 404 256
192.168.0.1 - - [12/Jun/2023:10:04:05 +0000] "GET /products.html HTTP/1.1" 200 4096
198.51.100.22 - - [12/Jun/2023:10:05:47 +0000] "GET /index.html HTTP/1.1" 500 1024
172.16.0.7 - - [12/Jun/2023:10:06:58 +0000] "GET /index.html HTTP/1.1" 200 1024
192.0.2.44 - - [12/Jun/2023:10:07:11 +0000] "GET /downloads/file.zip HTTP/1.1" 200 8192
10.0.0.5 - - [12/Jun/2023:10:08:14 +0000] "GET /index.html HTTP/1.1" 200 1024
203.0.113.10 - - [12/Jun/2023:10:09:33 +0000] "GET /blog HTTP/1.1" 200 512
198.18.0.1 - - [12/Jun/2023:10:10:02 +0000] "GET /index.html HTTP/1.1" 404 256
127.0.0.1 - - [12/Jun/2023:10:10:30 +0000] "GET /server-status HTTP/1.1" 200 1024
192.168.0.1 - - [12/Jun/2023:10:11:44 +0000] "GET /pricing.html HTTP/1.1" 404 256
172.16.0.7 - - [12/Jun/2023:10:12:15 +0000] "POST /api/data HTTP/1.1" 500 128
192.0.2.44 - - [12/Jun/2023:10:13:59 +0000] "GET /downloads/file2.zip HTTP/1.1" 200 4096
192.168.0.1 - - [12/Jun/2023:10:14:26 +0000] "GET /index.html HTTP/1.1" 200 1024
203.0.113.10 - - [12/Jun/2023:10:15:55 +0000] "GET /contact.html HTTP/1.1" 404 256
10.0.0.5 - - [12/Jun/2023:10:16:37 +0000] "GET /search?q=test HTTP/1.1" 200 512
198.51.100.22 - - [12/Jun/2023:10:17:48 +0000] "GET /index.html HTTP/1.1" 500 1024
198.18.0.1 - - [12/Jun/2023:10:18:25 +0000] "GET /docs/manual.pdf HTTP/1.1" 200 2048
172.16.0.7 - - [12/Jun/2023:10:19:11 +0000] "GET /support HTTP/1.1" 200 1024
192.168.0.1 - - [12/Jun/2023:10:20:48 +0000] "POST /login HTTP/1.1" 302 512
127.0.0.1 - - [12/Jun/2023:10:21:30 +0000] "GET /server-status HTTP/1.1" 200 1024
10.0.0.5 - - [12/Jun/2023:10:22:07 +0000] "GET /index.html HTTP/1.1" 404 256
203.0.113.10 - - [12/Jun/2023:10:23:59 +0000] "GET /blog HTTP/1.1" 200 512
192.168.0.1 - - [12/Jun/2023:10:24:26 +0000] "GET /index.html HTTP/1.1" 200 1024
198.51.100.22 - - [12/Jun/2023:10:25:48 +0000] "GET /health HTTP/1.1" 200 128
192.168.0.1 - - [12/Jun/2023:10:26:15 +0000] "GET /dashboard HTTP/1.1" 200 1024
10.0.0.5 - - [12/Jun/2023:10:27:37 +0000] "GET /search?q=linux HTTP/1.1" 500 256
203.0.113.11 - - [12/Jun/2023:10:28:48 +0000] "GET /index.html HTTP/1.1" 200 1024
192.0.2.45 - - [12/Jun/2023:10:29:29 +0000] "GET /robots.txt HTTP/1.1" 404 128
EOF

RUN chmod 644 /home/user/server_logs/access.log
RUN chmod 755 /home/user

LABEL Author="Apptainer Build Script"
LABEL Description="Initial state for web-server log analysis task with pytest pre-installed"