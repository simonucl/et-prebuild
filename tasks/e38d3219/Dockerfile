FROM ubuntu:22.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        gnupg \
        coreutils \
        gawk \
        sed && \
    pip3 install --no-cache-dir pytest

# Create the directory structure
RUN mkdir -p /home/user/logs

# Create the raw telemetry file with exact, byte-perfect content
RUN cat >/home/user/logs/resource_usage_2023-08-04.log <<'EOF'
2023-08-04 00:00:00 CPU=17% MEM=2048MB NET_IN=120kB/s NET_OUT=80kB/s
2023-08-04 06:00:00 CPU=65% MEM=4096MB NET_IN=512kB/s NET_OUT=340kB/s
2023-08-04 12:00:00 CPU=89% MEM=8192MB NET_IN=1024kB/s NET_OUT=840kB/s
2023-08-04 18:00:00 CPU=4% MEM=1024MB NET_IN=12kB/s NET_OUT=8kB/s
2023-08-04 23:59:59 CPU=52% MEM=6144MB NET_IN=256kB/s NET_OUT=210kB/s
EOF

# Ensure correct permissions (readable by all, writable by user)
RUN chmod 644 /home/user/logs/resource_usage_2023-08-04.log

# Create placeholder parent directory for future output (empty for now)
RUN mkdir -p /home/user/output && \
    chmod 755 /home/user/output

# Clean up apt cache to reduce image size
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/user