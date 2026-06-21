FROM ubuntu:22.04

# Author: Incident-Responder Exercise Team
# Description: Base image for the “internal TLS certificate” hands-on task

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/certs

RUN cat > /home/user/certs/server_info.txt <<'EOF'
Subject: CN=www.acme-inc.internal
Not Before: Jun 15 00:00:00 2023 GMT
Not After : Jun 15 23:59:59 2025 GMT
Serial    : 65A9C3
EOF

RUN chmod -R a+rwX /home/user && \
    chmod 755 /home/user