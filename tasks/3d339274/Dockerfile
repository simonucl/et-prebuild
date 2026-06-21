# Author: network-debug-initializer
# Description: Container prepared for the network-debug backup exercise: creates initial log files and installs pytest.
# Help: This container sets up the starting filesystem state for the "network-debug backup" exercise and installs pytest for automated verification.

FROM ubuntu:22.04

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/debug_logs && \
    chmod 755 /home/user && \
    chmod 755 /home/user/debug_logs

RUN cat > /home/user/debug_logs/ping.log <<'EOF'
PING google.com (142.250.72.46) 56(84) bytes of data.
64 bytes from lga34s34-in-f14.1e100.net (142.250.72.46): icmp_seq=1 ttl=115 time=12.3 ms
64 bytes from lga34s34-in-f14.1e100.net (142.250.72.46): icmp_seq=2 ttl=115 time=12.7 ms

--- google.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 12.302/12.509/12.716/0.207 ms
EOF

RUN cat > /home/user/debug_logs/traceroute.log <<'EOF'
traceroute to google.com (142.250.72.46), 30 hops max, 60 byte packets
 1  192.168.1.1 (192.168.1.1)  2.123 ms  2.112 ms  2.099 ms
 2  10.10.0.1 (10.10.0.1)  10.415 ms  10.394 ms  10.374 ms
 3  142.250.72.46 (142.250.72.46)  15.467 ms  15.451 ms  15.432 ms
EOF

RUN cat > /home/user/debug_logs/interface_status.log <<'EOF'
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.100  netmask 255.255.255.0  broadcast 192.168.1.255
        RX packets 1024  bytes 123456 (120.5 KiB)
        TX packets 1000  bytes 110000 (107.4 KiB)
EOF

RUN chmod 644 /home/user/debug_logs/*.log