FROM ubuntu:22.04

# Author="Container Build Script"
# Description="Environment for firewall incident responder task with pytest pre-installed."

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/logs

RUN cat >/home/user/logs/fw-incident-20240612.csv <<'EOF'
timestamp,src_ip,dst_ip,protocol,action,bytes
2024-06-12T08:55:01Z,10.0.0.15,172.16.0.1,ICMP,Blocked,0
2024-06-12T09:01:17Z,192.168.1.22,172.16.0.5,TCP,Allowed,1500
2024-06-12T09:02:45Z,203.0.113.45,172.16.0.7,TCP,Blocked,0
2024-06-12T09:05:30Z,198.51.100.12,172.16.0.9,UDP,Blocked,0
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/logs && \
    chmod 644 /home/user/logs/fw-incident-20240612.csv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

LABEL Author="Container Build Script"
LABEL Description="Environment for firewall incident responder task with pytest pre-installed."