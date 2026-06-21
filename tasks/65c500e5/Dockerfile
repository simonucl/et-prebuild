# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Exercise preparation script" \
      Description="Base image with initial state for certificate parsing task (pytest included)"

# Install Python 3, pip, and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial exercise directory structure and seed data
RUN mkdir -p /home/user/targets && \
    mkdir -p /home/user/audit

# Create the canonical certificate-dump text file
RUN cat > /home/user/targets/old_server_certificate.txt <<'EOF'
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            04:00:00:00:00:01 (268435457)
    Signature Algorithm: sha256WithRSAEncryption
        Issuer: CN=Old Vulnerable Server
        Validity
            Not Before: Apr  1 00:00:00 2022 GMT
            Not After : Apr  1 00:00:00 2023 GMT
        Subject: CN=Old Vulnerable Server
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (2048 bit)
                Modulus:
                    00:c6:33:24:2a:4c:5e:3b:c5:70:b0...
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Basic Constraints:
                CA:TRUE
            X509v3 Key Usage: critical
                Digital Signature, Key Cert Sign, CRL Sign
    Signature Algorithm: sha256WithRSAEncryption
         53:71:a1:9a:ce:9b:9a:8c:44:6b:c4:49:73:41:69...
-----END CERTIFICATE-----
EOF

# Set permissions: directories 0755, files 0644
RUN chmod 755 /home/user /home/user/targets /home/user/audit && \
    chmod 644 /home/user/targets/old_server_certificate.txt