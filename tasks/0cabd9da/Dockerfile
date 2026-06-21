FROM ubuntu:22.04

# Author: network-engineer-task
# Description: Initial state container for the quick network backup exercise

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        iputils-ping && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    mkdir -p /home/user/device_configs

RUN cat > /home/user/device_configs/router1.cfg <<'EOF'
hostname Router1
interface eth0
 ip address 10.0.0.1/24
!
EOF

RUN cat > /home/user/device_configs/router2.cfg <<'EOF'
hostname Router2
interface eth0
 ip address 10.0.1.1/24
!
EOF

RUN mkdir -p /home/user/net_backups && \
    chmod 755 /home/user && \
    chmod -R 755 /home/user/device_configs && \
    chmod -R 777 /home/user/net_backups

ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

LABEL Author="network-engineer-task"
LABEL Description="Initial state container for the quick network backup exercise"