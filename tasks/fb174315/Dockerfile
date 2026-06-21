FROM ubuntu:22.04

# Help / metadata from %labels
LABEL Author="Capacity-Planning Exercise Container"
LABEL Description="Provides initial state for capacity CSV extraction task."

# Environment variables from %environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/data

RUN cat << 'EOF' > /home/user/data/server_capacity.raw
MemTotal: 16384
MemFree: 8192
DiskTotal: 200G
DiskUsed: 120G
EOF

RUN chmod 0644 /home/user/data/server_capacity.raw && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/data