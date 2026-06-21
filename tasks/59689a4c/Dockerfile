# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels
LABEL Author="Container Generator"
LABEL Description="Environment for distributed-systems incident review exercise with pre-loaded dataset and pytest installed."

# Base packages and Python tooling
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        locales && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/data

# Exercise dataset
RUN cat > /home/user/data/logs.csv <<'EOF'
timestamp,node_id,level,message
2023-01-01T00:00:00Z,node-1,INFO,Service started
2023-01-01T00:01:00Z,node-2,ERROR,Unable to reach DB
2023-01-01T00:02:00Z,node-1,ERROR,Timeout
2023-01-01T00:03:00Z,node-2,WARN,High memory
2023-01-01T00:04:00Z,node-3,ERROR,Disk full
2023-01-01T00:05:00Z,node-1,INFO,Service heartbeat
2023-01-01T00:06:00Z,node-2,ERROR,Connection reset
2023-01-01T00:07:00Z,node-3,INFO,Service started
2023-01-01T00:08:00Z,node-1,ERROR,Out of memory
2023-01-01T00:09:00Z,node-1,ERROR,Service crashed
EOF

# Output directory placeholder and permissions
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked mkdir -p /home/user/output && \
    chmod -R 0755 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Default command (equivalent to %runscript)
CMD ["/bin/bash"]