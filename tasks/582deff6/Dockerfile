FROM ubuntu:22.04

# Labels
LABEL Author="chatGPT"
LABEL Description="Container for certificate-expiry report task — initial state ready for testing."

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates \
        tzdata && \
    pip3 install --no-cache-dir pytest

# Create the user's home hierarchy if it does not already exist
RUN mkdir -p /home/user

# diagnostics directory must be writable by the runtime (non-root) user
RUN mkdir -p /home/user/diagnostics/certs && \
    chmod 777 /home/user/diagnostics

# Seed the certificate files with the expected contents - db.crt
RUN cat > /home/user/diagnostics/certs/db.crt <<'EOF'
-----BEGIN CERTIFICATE-----
MIIDFA...
NotAfter=2024-12-31T23:59:59Z
-----END CERTIFICATE-----
EOF

# Seed the certificate files with the expected contents - webapp.crt
RUN cat > /home/user/diagnostics/certs/webapp.crt <<'EOF'
-----BEGIN CERTIFICATE-----
MIIDFA...
NotAfter=2026-06-11T12:00:00Z
-----END CERTIFICATE-----
EOF

# Make sure everything is world-readable
RUN chmod -R a+r /home/user/diagnostics/certs

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:$PATH

# Help information (as comment):
# This container image provides the initial filesystem state for the
# certificate-expiry report exercise.