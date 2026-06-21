FROM ubuntu:22.04

# Install Python tooling and pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state
RUN mkdir -p /home/user/network/logs

# Populate diag.log with the reference ping reports
RUN cat > /home/user/network/logs/diag.log <<'EOF'
PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=0.834 ms

--- 192.168.1.1 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4081ms
    chmod 755 /home/user

rtt min/avg/max/mdev = 0.620/0.699/0.834/0.083 ms

PING 10.0.0.5 (10.0.0.5) 56(84) bytes of data.
From 10.0.0.1 icmp_seq=1 Destination Host Unreachable
From 10.0.0.1 icmp_seq=2 Destination Host Unreachable
From 10.0.0.1 icmp_seq=3 Destination Host Unreachable

--- 10.0.0.5 ping statistics ---
3 packets transmitted, 0 received, +3 errors, 100% packet loss, time 2035ms

PING 172.16.0.7 (172.16.0.7) 56(84) bytes of data.
64 bytes from 172.16.0.7: icmp_seq=1 ttl=62 time=5.15 ms
64 bytes from 172.16.0.7: icmp_seq=2 ttl=62 time=5.10 ms

--- 172.16.0.7 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4091ms
rtt min/avg/max/mdev = 5.103/5.149/5.196/0.046 ms

PING 192.168.2.200 (192.168.2.200) 56(84) bytes of data.
From 192.168.2.1 icmp_seq=1 Destination Host Unreachable
From 192.168.2.1 icmp_seq=2 Destination Host Unreachable
From 192.168.2.1 icmp_seq=3 Destination Host Unreachable

--- 192.168.2.200 ping statistics ---
3 packets transmitted, 0 received, +3 errors, 100% packet loss, time 3034ms
EOF

# Fix permissions
RUN chmod 644 /home/user/network/logs/diag.log

LABEL Author="ping-diagnostics-setup"
LABEL Description="Environment prepared for the ping-diagnostics task (pytest included)"