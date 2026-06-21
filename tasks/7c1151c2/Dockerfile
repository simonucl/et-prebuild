FROM ubuntu:22.04

# Basic tooling
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create user and directories
RUN useradd -m -d /home/user -s /bin/bash user && \
    mkdir -p /home/user/server_logs

# Populate log file
RUN cat > /home/user/server_logs/app.log <<'APPLOG'
2023-04-29 11:22:33 [INFO]  (192.168.1.10) status=200 Request processed successfully
2023-04-29 11:22:34 [ERROR] (192.168.1.11) status=500 Internal server error
2023-04-29 11:22:35 [WARN]  (192.168.1.12) status=404 Resource not found
2023-04-29 11:22:36 [ERROR] (10.0.0.5)     status=503 Service unavailable
2023-04-29 11:22:37 [INFO]  (192.168.1.10) status=200 Request processed successfully
2023-04-29 11:22:38 [ERROR] (172.16.0.2)   status=501 Not implemented
2023-04-29 11:22:39 [INFO]  (192.168.1.15) status=302 Redirect
2023-04-29 11:22:40 [ERROR] (192.168.1.11) status=500 Internal server error
2023-04-29 11:22:41 [INFO]  (192.168.1.10) status=200 Request processed successfully
2023-04-29 11:22:42 [ERROR] (10.0.0.5)     status=504 Gateway timeout
APPLOG

# Permissions
RUN chmod 644 /home/user/server_logs/app.log && \
    chmod 755 /home/user/server_logs && \
    chmod 777 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8