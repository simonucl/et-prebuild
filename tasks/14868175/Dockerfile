FROM ubuntu:22.04

# Help / description
# Author="container-prep"
# Description="Environment for ICMP statistics parsing assignment – provides pytest and the initial ping_results.txt fixture."

ENV LC_ALL=C
ENV PYTHONIOENCODING=utf-8

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/network

RUN cat > /home/user/network/ping_results.txt <<'EOF'
PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=0.123 ms
64 bytes from 192.168.1.1: icmp_seq=2 ttl=64 time=0.112 ms

--- 192.168.1.1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms

PING 10.0.0.1 (10.0.0.1) 56(84) bytes of data.
From 10.0.0.100 icmp_seq=1 Destination Host Unreachable
From 10.0.0.100 icmp_seq=2 Destination Host Unreachable

--- 10.0.0.1 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 2ms

PING 172.16.0.1 (172.16.0.1) 56(84) bytes of data.
64 bytes from 172.16.0.1: icmp_seq=1 ttl=64 time=1.345 ms
From 172.16.0.1 icmp_seq=2 Destination Host Unreachable

--- 172.16.0.1 ping statistics ---
2 packets transmitted, 1 received, 50% packet loss, time 2002ms
EOF

RUN chmod 755 /home && \
    chmod 755 /home/user && \
    chmod 755 /home/user/network && \
    chmod 644 /home/user/network/ping_results.txt