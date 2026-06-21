FROM ubuntu:22.04

# Author: network-backup-container
# Description: Container providing initial state for the network backup exercise

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/net_logs && \
    chmod 0777 /home/user

RUN cat >/home/user/net_logs/ping_output.txt <<'EOF'
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=115 time=12.3 ms
EOF

RUN cat >/home/user/net_logs/traceroute_output.txt <<'EOF'
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max
 1  10.0.0.1 (10.0.0.1)  1.123 ms
 2  8.8.8.8 (8.8.8.8)  12.345 ms
EOF

RUN chmod 0644 /home/user/net_logs/*.txt

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin