FROM ubuntu:22.04

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/pentest

RUN cat >/home/user/pentest/.targets.env <<'EOF'
TARGET_A=192.168.1.10
TARGET_B=10.0.0.5
PORTS=22,80,443
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/pentest && \
    chmod 644 /home/user/pentest/.targets.env

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH