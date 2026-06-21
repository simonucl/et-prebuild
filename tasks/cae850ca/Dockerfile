FROM ubuntu:22.04

# Author="Container Preparation Bot"
# Description="Environment for the 'Symlink Management & 404-Error Summary for Archived Web Logs' task with pre-populated Apache log archives and pytest installed."

# Ensure Python is in PATH
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Install Python, pip and pytest
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare directory tree
RUN install -d -m 0777 /home/user && \
    install -d -m 0755 /home/user/archive_logs && \
    install -d -m 0755 /home/user/archive_logs/2023-07-01 && \
    install -d -m 0755 /home/user/archive_logs/2023-07-02 && \
    install -d -m 0755 /home/user/archive_logs/2023-07-03

# Create log file for 2023-07-01
RUN cat > /home/user/archive_logs/2023-07-01/access.log <<'EOF'
127.0.0.1 - - [01/Jul/2023:00:00:01 +0000] "GET /index.html HTTP/1.1" 200 1024
192.168.1.10 - - [01/Jul/2023:00:02:34 +0000] "GET /about HTTP/1.1" 404 512
10.0.0.5 - - [01/Jul/2023:00:04:55 +0000] "GET /contact HTTP/1.1" 404 256
127.0.0.1 - - [01/Jul/2023:00:06:12 +0000] "GET /home HTTP/1.1" 200 1024
192.168.1.10 - - [01/Jul/2023:00:07:21 +0000] "GET /privacy HTTP/1.1" 404 128
10.0.0.5 - - [01/Jul/2023:00:08:09 +0000] "GET /terms HTTP/1.1" 404 256
127.0.0.1 - - [01/Jul/2023:00:10:02 +0000] "GET /api/data HTTP/1.1" 200 2048
192.168.1.10 - - [01/Jul/2023:00:11:42 +0000] "GET /faq HTTP/1.1" 404 128
127.0.0.1 - - [01/Jul/2023:00:13:33 +0000] "GET /blog HTTP/1.1" 200 512
10.0.0.5 - - [01/Jul/2023:00:15:27 +0000] "GET /download HTTP/1.1" 200 4096
# 404 count = 5
EOF

RUN chmod 0644 /home/user/archive_logs/2023-07-01/access.log

# Create log file for 2023-07-02
RUN cat > /home/user/archive_logs/2023-07-02/access.log <<'EOF'
127.0.0.1 - - [02/Jul/2023:01:11:11 +0000] "GET /index.html HTTP/1.1" 200 1024
10.0.0.5 - - [02/Jul/2023:01:12:12 +0000] "GET /foo HTTP/1.1" 404 256
192.168.1.10 - - [02/Jul/2023:01:13:13 +0000] "GET /bar HTTP/1.1" 200 2048
127.0.0.1 - - [02/Jul/2023:01:14:14 +0000] "GET /baz HTTP/1.1" 404 128
10.0.0.5 - - [02/Jul/2023:01:15:15 +0000] "GET /xyz HTTP/1.1" 200 1024
192.168.1.10 - - [02/Jul/2023:01:16:16 +0000] "GET /abc HTTP/1.1" 404 256
127.0.0.1 - - [02/Jul/2023:01:17:17 +0000] "GET /def HTTP/1.1" 200 512
10.0.0.5 - - [02/Jul/2023:01:18:18 +0000] "GET /ghi HTTP/1.1" 200 1024
192.168.1.10 - - [02/Jul/2023:01:19:19 +0000] "GET /jkl HTTP/1.1" 200 2048
127.0.0.1 - - [02/Jul/2023:01:20:20 +0000] "GET /mno HTTP/1.1" 200 512
# 404 count = 3
EOF

RUN chmod 0644 /home/user/archive_logs/2023-07-02/access.log

# Create log file for 2023-07-03
RUN cat > /home/user/archive_logs/2023-07-03/access.log <<'EOF'
127.0.0.1 - - [03/Jul/2023:02:21:01 +0000] "GET /one HTTP/1.1" 404 128
10.0.0.5 - - [03/Jul/2023:02:22:02 +0000] "GET /two HTTP/1.1" 404 256
192.168.1.10 - - [03/Jul/2023:02:23:03 +0000] "GET /three HTTP/1.1" 404 512
127.0.0.1 - - [03/Jul/2023:02:24:04 +0000] "GET /four HTTP/1.1" 404 1024
10.0.0.5 - - [03/Jul/2023:02:25:05 +0000] "GET /five HTTP/1.1" 404 256
192.168.1.10 - - [03/Jul/2023:02:26:06 +0000] "GET /six HTTP/1.1" 200 1024
127.0.0.1 - - [03/Jul/2023:02:27:07 +0000] "GET /seven HTTP/1.1" 404 128
10.0.0.5 - - [03/Jul/2023:02:28:08 +0000] "GET /eight HTTP/1.1" 404 256
192.168.1.10 - - [03/Jul/2023:02:29:09 +0000] "GET /nine HTTP/1.1" 404 512
127.0.0.1 - - [03/Jul/2023:02:30:10 +0000] "GET /ten HTTP/1.1" 200 1024
# 404 count = 8
EOF

RUN chmod 0644 /home/user/archive_logs/2023-07-03/access.log

# Clean up apt cache to reduce image size
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set permissions on /home/user
RUN chmod 755 /home/user