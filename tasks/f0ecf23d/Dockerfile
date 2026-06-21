FROM ubuntu:22.04

# Help text
# This Apptainer container sets up the initial state for the “network-diagnostic”
# exercise. It provides the required sample captures under /home/user/net_samples
# and has pytest pre-installed so that the supplied verification suite can be run
# immediately after the container is started.
# Author: network-diagnostic-initial-state

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/net_samples && \
    chmod 1777 /home/user

RUN cat <<'EOF' > /home/user/net_samples/ping4.txt
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=20.3 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=117 time=20.1 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=117 time=19.8 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=117 time=19.9 ms

--- 8.8.8.8 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 9ms
    chmod 755 /home/user

rtt min/avg/max/mdev = 19.800/20.025/20.300/0.200 ms
EOF

RUN cat <<'EOF' > /home/user/net_samples/ping6.txt
PING 2001:4860:4860::8888(2001:4860:4860::8888): 56 data bytes
64 bytes from 2001:4860:4860::8888: icmp_seq=1 ttl=117 time=30.3 ms
64 bytes from 2001:4860:4860::8888: icmp_seq=2 ttl=117 time=30.1 ms
64 bytes from 2001:4860:4860::8888: icmp_seq=3 ttl=117 time=29.8 ms
64 bytes from 2001:4860:4860::8888: icmp_seq=4 ttl=117 time=29.9 ms

--- 2001:4860:4860::8888 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 12ms
rtt min/avg/max/mdev = 29.800/30.025/30.300/0.200 ms
EOF

RUN cat <<'EOF' > /home/user/net_samples/ss.txt
Netid State      Recv-Q Send-Q Local Address:Port               Peer Address:Port
tcp   LISTEN     0      128    0.0.0.0:22                       0.0.0.0:*
tcp   LISTEN     0      128    [::]:22                          [::]:*
tcp   ESTAB      0      0      192.168.1.2:22                   192.168.1.10:54321
tcp   ESTABLISHED 0     0      192.168.1.2:22                   192.168.1.11:54322
tcp   TIME-WAIT  0      0      192.168.1.2:12345                192.168.1.12:80
EOF

RUN chmod 644 /home/user/net_samples/*.txt