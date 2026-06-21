FROM ubuntu:22.04

# Author inventory-builder setup
# Description Base environment for the “inventory-builder” exercise.

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        ca-certificates \
        tzdata && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/provision/output && \
    chmod 755 /home/user && \
    chmod 755 /home/user/provision && \
    chmod 755 /home/user/provision/output

RUN cat > /home/user/provision/servers_raw.txt << 'EOF'
DB01
web01
app02
web01
app01
db01
WEB02
app02
EOF

RUN chmod 644 /home/user/provision/servers_raw.txt

LABEL Author="inventory-builder setup"
LABEL Description="Base environment for the inventory-builder exercise."