FROM ubuntu:22.04

# Author log-cleanup exercise maintainer
# Description Base image for the "regex log-cleanup" task

# Ensure the build is non-interactive
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/datasets/log_cleanup

# Create the raw log file
RUN cat > /home/user/datasets/log_cleanup/raw_web_events.log << 'EOF'
192.168.0.10 - - [12/Mar/2024:12:00:01 +0000] "GET /index.html HTTP/1.1" 200 1024
10.0.0.5 - - [12/Mar/2024:12:00:03 +0000] "POST /login HTTP/1.1" 302 512
172.16.0.12 - - [12/Mar/2024:12:00:05 +0000] "GET /dashboard HTTP/1.1" 200 2048
invalid_line this should be removed
203.0.113.1 - - [12/Mar/2024:12:00:08 +0000] "GET /secret HTTP/1.1 user@example.com" 200 300
198.51.100.23 - - [12/Mar/2024:12:00:10 +0000] "GET /contact HTTP/1.1" 200 128
192.0.2.44 - - [12/Mar/2024:12:00:12 +0000] "GET /product/123456789 HTTP/1.1" 200 500
203.0.113.2 - - [12/Mar/2024:12:00:14 +0000] "POST /api/update HTTP/1.1" 200 1500
198.51.100.24 - - [12/Mar/2024:12:00:16 +0000] "GET /contact HTTP/1.1" 200 180
192.0.2.45 - - [12/Mar/2024:12:00:18 +0000] "GET /download HTTP/1.1" 404 0
198.18.0.1 - - [12/Mar/2024:12:00:20 +0000] "GET /docs HTTP/1.1" 200 2048
198.51.100.25 - - [12/Mar/2024:12:00:22 +0000] "GET /privacy HTTP/1.1 555-123-4567" 200 200
This is another bad line 1234
192.168.0.256 - - [12/Mar/2024:12:00:24 +0000] "GET /invalid-ip HTTP/1.1" 400 0
203.0.113.3 - - [12/Mar/2024:12:00:26 +0000] "POST /logout HTTP/1.1" 200 256
EOF

# Give the future unprivileged user full access to the working area
RUN chmod -R a+rwx /home/user || true

# Clean up apt caches to reduce image size
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1

WORKDIR /home/user