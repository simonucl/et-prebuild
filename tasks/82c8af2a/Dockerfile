FROM ubuntu:22.04

# Basic tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip \
    diffutils patch \
    ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Prepare initial directory tree
RUN mkdir -p /home/user/network_configs/baseline \
             /home/user/network_configs/current \
             /home/user/network_configs/logs \
             /home/user/network_configs/patches

# baseline/router.conf
RUN cat > /home/user/network_configs/baseline/router.conf <<'EOF'
hostname Router01
interface eth0
 ip address 10.0.0.1/24
 no shutdown
!
interface eth1
 ip address 192.168.1.1/24
 shutdown
!
router ospf
 network 10.0.0.0 0.0.0.255 area 0
 network 192.168.1.0 0.0.0.255 area 0
!
EOF

# current/router.conf
RUN cat > /home/user/network_configs/current/router.conf <<'EOF'
hostname Router01
interface eth0
 ip address 10.0.0.2/24
 shutdown
!
interface eth1
 ip address 192.168.1.1/24
 shutdown
!
router ospf
 network 10.0.0.0 0.0.0.255 area 0
!
EOF

# Permissions
RUN chmod -R 755 /home/user && \
    find /home/user -type f -exec chmod 644 {} \;

# Environment variables
ENV PATH="$PATH:/usr/local/bin"

CMD echo "This container is prepared for the network configuration patch task." && \
    echo "You can now follow the instructions to create and apply the patch."