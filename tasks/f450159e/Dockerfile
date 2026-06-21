FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/logs && \
    chmod 755 /home/user/logs

RUN cat > /home/user/logs/server.log <<'EOF'
2023-10-01 12:00:00Z INFO server1 GET /api/user 200 123ms
2023-10-01 12:05:00Z WARN server1 POST /api/order 500 98ms
2023-10-01 12:10:00Z INFO server2 GET /api/product 200 110ms
2023-10-01 12:15:00Z ERROR server2 DELETE /api/order 404 130ms
EOF

RUN chmod 644 /home/user/logs/server.log

ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1