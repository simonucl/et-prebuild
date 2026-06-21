# Help: This container provides the initial environment for the networking
# rsync exercise. It contains:
#   - /home/user/source_configs/ (three *.conf files)
#   - /home/user/remote_share/site_backup/ (empty)
#   - /home/user/logs/ (empty)
# Required utilities (rsync, ping) and pytest are pre‑installed.

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        rsync \
        iputils-ping \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/source_configs && \
    mkdir -p /home/user/remote_share/site_backup && \
    mkdir -p /home/user/logs

RUN cat <<'EOF' > /home/user/source_configs/router1.conf
hostname Router1
interface Gig0/0/0
 ip address 10.0.1.1 255.255.255.0
!
EOF

RUN cat <<'EOF' > /home/user/source_configs/router2.conf
hostname Router2
interface Gig0/0/0
 ip address 10.0.2.1 255.255.255.0
!
EOF

RUN cat <<'EOF' > /home/user/source_configs/router3.conf
hostname Router3
interface Gig0/0/0
 ip address 10.0.3.1 255.255.255.0
!
EOF

RUN chmod -R 0777 /home/user