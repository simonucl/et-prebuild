FROM ubuntu:22.04

# Author ChatGPT
# Description "Base image for certificate-maintenance task; supplies initial /home/user/certs dataset and pytest"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/certs && \
    chmod 755 /home/user && \
    chmod 755 /home/user/certs

RUN cat > /home/user/certs/alpha.pem <<'EOF'
-----BEGIN CERTIFICATE-----
Dummy certificate placeholder only for testing utilities.
Serial Number: 01
Not After : 2030-12-31 23:59:59 GMT
Subject CN=alpha.example.io
-----END CERTIFICATE-----
EOF

RUN cat > /home/user/certs/beta.pem <<'EOF'
-----BEGIN CERTIFICATE-----
Dummy certificate placeholder only for testing utilities.
Serial Number: 02
Not After : 2025-06-15 12:00:00 GMT
Subject CN=beta.example.io
-----END CERTIFICATE-----
EOF

RUN chmod 644 /home/user/certs/alpha.pem /home/user/certs/beta.pem

ENV PYTHONIOENCODING=UTF-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8