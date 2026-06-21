FROM ubuntu:22.04

# Labels
LABEL Author="ChatGPT"
LABEL Description="Initial container state for bare-metal provisioning workflow task"

RUN set -eu && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/provisioning/input && \
    mkdir -p /home/user/provisioning/output

RUN cat <<'EOF' > /home/user/provisioning/input/servers.csv
host,ip,cpu,ram
web01,10.10.1.11,4,16
db01,10.10.1.12,8,32
cache01,10.10.1.13,2,8
EOF

RUN cat <<'EOF' > /home/user/provisioning/input/network.csv
ip,vlan,subnet
10.10.1.11,frontend,10.10.1.0/24
10.10.1.12,backend,10.10.1.0/24
10.10.1.13,cache,10.10.1.0/24
EOF

RUN chmod 644 /home/user/provisioning/input/*.csv && \
    chmod 777 /home/user/provisioning/output && \
    chmod 755 /home/user/provisioning /home/user/provisioning/input