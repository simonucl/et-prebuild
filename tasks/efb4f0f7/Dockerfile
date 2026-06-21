FROM ubuntu:22.04

# Update package index and install Python tooling
RUN set -eux && \
    DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv

# Install pytest for the grading harness
RUN pip3 install --no-cache-dir pytest

# Create base home directory if missing and make it writable
RUN mkdir -p /home/user && chmod 777 /home/user

# Create ping-dump directory
RUN mkdir -p /home/user/network_dumps && chmod 755 /home/user/network_dumps

# ping_8.8.8.8.log
RUN cat <<'EOF' > /home/user/network_dumps/ping_8.8.8.8.log
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=118 time=14.176 ms

--- 8.8.8.8 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 14.176/14.176/14.176/0.000 ms
EOF

# ping_1.1.1.1.log
RUN cat <<'EOF' > /home/user/network_dumps/ping_1.1.1.1.log
PING 1.1.1.1 (1.1.1.1): 56 data bytes
64 bytes from 1.1.1.1: icmp_seq=0 ttl=57 time=12.652 ms

--- 1.1.1.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 12.652/12.652/12.652/0.000 ms
EOF

# ping_example.com.log
RUN cat <<'EOF' > /home/user/network_dumps/ping_example.com.log
PING example.com (93.184.216.34): 56 data bytes

--- example.com ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 0ms
EOF

RUN chmod 644 /home/user/network_dumps/ping_*.log

# Create log directory
RUN mkdir -p /home/user/netlogs && chmod 777 /home/user/netlogs

# Environment section empty in original
ENV HOME=/home/user

# Labels
LABEL Author="Automated build"
LABEL Description="Container for network troubleshooting assignment with initial ping dumps and pytest pre-installed."