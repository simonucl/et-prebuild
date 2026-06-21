FROM ubuntu:22.04

# Help text from %help
# Container for the “ping report” clean-up task.
# Provides /home/user/network/ping_report.log for students to process
# and has pytest installed for the grading infrastructure.

LABEL Author="example"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/network

RUN cat > /home/user/network/ping_report.log <<'EOF'
PING google.com (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=117 time=11.813 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=10.978 ms
Request timeout for icmp_seq 2

---
PING cloudflare.com (1.1.1.1): 56 data bytes
64 bytes from 1.1.1.1: icmp_seq=0 ttl=58 time=7.216 ms
Request timeout for icmp_seq 1
64 bytes from 1.1.1.1: icmp_seq=2 ttl=58 time=7.143 ms

---
PING invalidhost (203.0.113.10): 56 data bytes
Request timeout for icmp_seq 0
Request timeout for icmp_seq 1

---
From 192.168.0.1 icmp_seq=3 Destination Host Unreachable
EOF

RUN chmod 0755 /home/user/network && \
    chmod 0644 /home/user/network/ping_report.log