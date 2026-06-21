FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer task prep"
LABEL Description="Container providing initial state for the network-diagnostics summary exercise"

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Base OS packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Python tooling – pytest for the grader
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# Prepare initial exercise data
RUN mkdir -p /home/user/network_diagnostics/raw

# ping_localhost.txt
RUN cat > /home/user/network_diagnostics/raw/ping_localhost.txt <<'EOF'
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.026 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.031 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.025 ms
64 bytes from 127.0.0.1: icmp_seq=4 ttl=64 time=0.035 ms

--- 127.0.0.1 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3058ms
rtt min/avg/max/mdev = 0.025/0.029/0.035/0.004 ms
EOF

# traceroute_localhost.txt
RUN cat > /home/user/network_diagnostics/raw/traceroute_localhost.txt <<'EOF'
traceroute to 127.0.0.1 (127.0.0.1), 30 hops max, 60 byte packets
 1  localhost (127.0.0.1) 0.031 ms 0.014 ms 0.012 ms
EOF

# ss_output.txt
RUN cat > /home/user/network_diagnostics/raw/ss_output.txt <<'EOF'
Netid  State      Recv-Q Send-Q Local Address:Port               Peer Address:Port              
udp    UNCONN     0      0              0.0.0.0:68                          0.0.0.0:*      users:(("dhclient",pid=658,fd=6))                                                    
tcp    LISTEN     0      128            0.0.0.0:22                          0.0.0.0:*      users:(("sshd",pid=744,fd=3))                                                      
tcp    LISTEN     0      128                  *:80                                *:*      users:(("nginx",pid=800,fd=4))                                                    
EOF

# Permissions: make sure non-root users can read/write these paths
RUN chmod -R 777 /home/user && \
    chmod 755 /home/user

WORKDIR /home/user