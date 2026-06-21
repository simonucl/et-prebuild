FROM ubuntu:22.04

# Install Python tooling and pytest for the checker
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial directory structure and log file
RUN mkdir -p /home/user/audit/logs

RUN cat > /home/user/audit/logs/access.log <<'EOF'
2023-10-01 12:00:01 userA login success
2023-10-01 12:00:05 userB login success
2023-10-01 12:02:11 userA login success
2023-10-01 12:05:41 userC login success
2023-10-01 12:15:00 userA login success
2023-10-01 12:20:22 userB login success
2023-10-01 12:30:33 userD login success
2023-10-01 12:45:54 userB login success
2023-10-01 12:50:01 userE login success
2023-10-01 13:00:11 userC login success
2023-10-01 13:05:19 userB login success
2023-10-01 13:15:45 userB login success
EOF

# Ensure read/write permissions
RUN chmod -R a+rwX /home/user && chmod 755 /home/user

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Help text
# Compliance log analysis container. Start a shell with:
#   docker run -it <image> bash