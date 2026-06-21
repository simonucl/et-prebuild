FROM ubuntu:22.04

ENV LC_ALL=C
ENV LANG=C

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/logs

RUN cat > /home/user/logs/node1.log <<'EOF'
2023-12-01T10:15:30Z INFO  node1 1001 Task started
2023-12-01T10:16:00Z ERROR node1 1001 OutOfMemory
2023-12-01T10:17:00Z INFO  node1 1002 Task started
2023-12-01T10:17:30Z ERROR node1 1002 Timeout
EOF

RUN cat > /home/user/logs/node2.log <<'EOF'
2023-12-01T10:20:10Z INFO  node2 2001 Task started
2023-12-01T10:21:00Z ERROR node2 2001 DiskFull
2023-12-01T10:22:00Z INFO  node2 2002 Task started
2023-12-01T10:22:30Z INFO  node2 2002 Task finished successfully
2023-12-01T10:23:00Z ERROR node2 2003 NetworkPartition
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/logs && \
    chmod 644 /home/user/logs/node1.log /home/user/logs/node2.log