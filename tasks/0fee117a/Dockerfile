# Converted from Apptainer definition file
FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare filesystem layout
RUN mkdir -p /home/user/backup/certs && \
    mkdir -p /home/user/certs && \
    chmod 755 /home/user /home/user/backup /home/user/backup/certs /home/user/certs

# Write certificate files
RUN cat >/home/user/backup/certs/rootCA.pem <<'EOF'
-----BEGIN CERTIFICATE-----
root-ca-placeholder
-----END CERTIFICATE-----
EOF

RUN cat >/home/user/backup/certs/intermediateCA.pem <<'EOF'
-----BEGIN CERTIFICATE-----
intermediate-ca-placeholder
-----END CERTIFICATE-----
EOF

RUN cat >/home/user/backup/certs/server.pem <<'EOF'
-----BEGIN CERTIFICATE-----
server-cert-placeholder
-----END CERTIFICATE-----
EOF

# Fix permissions
RUN chmod 644 /home/user/backup/certs/*.pem

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# Runtime message
CMD echo "Container ready for the TLS certificate restore exercise." && \
    echo "Run your restore script inside this container, then execute pytest to validate."