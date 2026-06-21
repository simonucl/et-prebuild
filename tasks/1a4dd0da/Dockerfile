FROM ubuntu:22.04

# Help/description from %runscript
# Container for the hostname-enrichment task.
# Input data is in /home/user/datasets and /home/user/resources.
# Write your results to /home/user/outputs.

RUN set -e && \
    mkdir -p /home/user/datasets && \
    mkdir -p /home/user/resources && \
    mkdir -p /home/user/outputs

RUN cat > /home/user/datasets/server_access.csv <<'EOF'
ip,timestamp,bytes_sent
192.0.2.1,2023-10-01T12:00:00Z,512
203.0.113.5,2023-10-01T12:01:00Z,1024
198.51.100.42,2023-10-01T12:02:00Z,2048
EOF

RUN cat > /home/user/resources/ip_hostname_map.txt <<'EOF'
192.0.2.1	api.internal.example
203.0.113.5	db01.internal.example
198.51.100.42	cache.internal.example
EOF

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user && \
    chmod -R 755 /home/user/datasets /home/user/resources && \
    chmod 777 /home/user/outputs

ENV HOME=/home/user