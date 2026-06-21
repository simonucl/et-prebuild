FROM ubuntu:22.04

# Author: OpenAI ChatGPT
# Description: Container prepared for awk/sed automation exercise with initial dataset and pytest installed.

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN set -eux && \
    mkdir -p /home/user/data && \
    mkdir -p /home/user/reports && \
    chmod 755 /home/user/data && \
    chmod 755 /home/user/reports && \
    chmod 755 /home/user

RUN cat > /home/user/data/servers.cfg <<'EOF'
server_id:srv-alpha   status=active   ip=10.10.1.11
server_id:srv-beta    status=inactive ip=10.10.1.12
server_id:srv-gamma   status=active   ip=10.10.1.13
server_id:srv-delta   status=inactive ip=10.10.1.14
server_id:srv-epsilon status=active   ip=10.10.1.15
EOF

RUN chmod 644 /home/user/data/servers.cfg

RUN cat > /home/user/data/ports.list <<'EOF'
22
80
443
8080
8443
3306
5432
EOF

RUN chmod 644 /home/user/data/ports.list

RUN cat > /home/user/data/provision.log <<'EOF'
2023-06-12T08:12:17Z Started provisioning alpha
2023-06-12T08:12:38Z alpha: packages installed
2023-06-12T08:13:01Z Finished provisioning alpha
2023-06-12T08:14:07Z Started provisioning beta
2023-06-12T08:14:42Z beta: dependency failure
2023-06-12T08:14:45Z Finished provisioning beta with error
EOF

RUN chmod 644 /home/user/data/provision.log