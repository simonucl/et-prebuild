FROM ubuntu:22.04

# Author "Apptainer Task Setup"
# Description "Initial state for router checksum verification exercise"

ENV PYTHONUNBUFFERED=1

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/network_configs && \
    chmod 755 /home/user && \
    chmod 755 /home/user/network_configs

RUN cat > /home/user/network_configs/router.cfg <<'EOF'
!
version 15.2
hostname TestRouter
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
!
end
EOF

RUN sha256sum /home/user/network_configs/router.cfg | awk '{print $1}' > /home/user/network_configs/router.cfg.sha256

RUN chmod 644 /home/user/network_configs/router.cfg && \
    chmod 644 /home/user/network_configs/router.cfg.sha256