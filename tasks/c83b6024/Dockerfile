# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help / labels from %labels
LABEL Author="incident-response-task"
LABEL Description="Base image for incident-response exercise with initial evidence and pytest installed"

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e \
 && apt-get update -qq \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
 && pip3 install --no-cache-dir pytest \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Create user and environment
RUN set -e \
 && if ! id -u 1000 >/dev/null 2>&1; then useradd -m -u 1000 -s /bin/bash user; fi \
 && mkdir -p /home/user/logs

# Create http-access-incident.log
RUN cat > /home/user/logs/http-access-incident.log <<'EOF'
192.168.1.50 - - [14/Jun/2024:02:15:23 +0000] "GET /admin/login.php HTTP/1.1" 404 560 "-" "Mozilla/5.0"
203.0.113.77 - - [14/Jun/2024:02:16:01 +0000] "POST /wp-login.php HTTP/1.1" 200 482 "-" "Mozilla/5.0"
198.51.100.23 - - [14/Jun/2024:02:16:22 +0000] "GET / HTTP/1.1" 200 762 "-" "curl/7.68.0"
EOF

# Create firewall-20240614.log
RUN cat > /home/user/logs/firewall-20240614.log <<'EOF'
Jun 14 02:15:24 host kernel: [UFW BLOCK] IN=eth0 OUT= MAC=00:0c:29:4f:8e:35 SRC=203.0.113.77 DST=192.168.1.10 LEN=60 TOS=0x00 PREC=0x00 TTL=47 ID=54321 DF PROTO=TCP SPT=55932 DPT=80 WINDOW=29200 RES=0x00 SYN URGP=0
Jun 14 02:16:10 host kernel: [UFW BLOCK] IN=eth0 OUT= MAC=00:0c:29:4f:8e:35 SRC=198.51.100.23 DST=192.168.1.10 LEN=60 TOS=0x00 PREC=0x00 TTL=49 ID=12345 DF PROTO=TCP SPT=49000 DPT=22 WINDOW=29200 RES=0x00 SYN URGP=0
EOF

# Fix permissions
RUN chmod -R a+rwX /home/user && chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8