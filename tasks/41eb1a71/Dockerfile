FROM ubuntu:22.04

# Author network-audit-container
# Description "Initial state for the 'Network connectivity audit with sort + uniq frequency counting' task."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        gzip \
        coreutils \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/network/logs

RUN cat >/tmp/connection_attempts.csv <<'EOF'
2023-10-12 09:00:01,10.0.0.5,8.8.8.8,ICMP,0,ACCEPT
2023-10-12 09:00:02,10.0.0.5,8.8.8.8,ICMP,0,ACCEPT
2023-10-12 09:00:03,10.0.0.5,8.8.4.4,ICMP,0,DROP
2023-10-12 09:00:04,10.0.0.5,1.1.1.1,ICMP,0,ACCEPT
2023-10-12 09:00:05,10.0.0.5,8.8.8.8,ICMP,0,DROP
2023-10-12 09:00:06,10.0.0.5,8.8.8.8,ICMP,0,DROP
2023-10-12 09:00:07,10.0.0.5,1.1.1.1,ICMP,0,ACCEPT
2023-10-12 09:00:08,10.0.0.5,8.8.4.4,ICMP,0,REJECT
2023-10-12 09:00:09,10.0.0.5,8.8.8.8,ICMP,0,ACCEPT
2023-10-12 09:00:10,10.0.0.5,8.8.8.8,ICMP,0,ACCEPT
EOF

RUN gzip -c /tmp/connection_attempts.csv > /home/user/network/logs/connection_attempts.csv.gz && \
    rm -f /tmp/connection_attempts.csv && \
    chmod 0777 /home/user/network && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin

CMD echo "Container for the Network Connectivity Audit task." && \
    echo "Run your commands or tests as needed."