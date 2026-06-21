FROM ubuntu:22.04

# Labels
LABEL Author="ExampleBuilder"
LABEL Description="Prepared environment for certificate triage task with pytest installed."

# Basic tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare starting filesystem state for the exercise
# Create the expected user home and incoming certificate directory
RUN mkdir -p /home/user/certs_incoming

# Create .meta files
RUN cat << 'EOF' > /home/user/certs_incoming/server_ok.meta
CN=api.example.com|CN=Example-CA|2023-06-01|2024-12-31
EOF

RUN cat << 'EOF' > /home/user/certs_incoming/server_soon.meta
CN=login.example.com|CN=Example-CA|2023-07-01|2024-07-01
EOF

RUN cat << 'EOF' > /home/user/certs_incoming/server_expired.meta
CN=legacy.example.com|CN=Legacy-CA|2022-05-01|2023-12-31
EOF

# Create dummy .crt files (PEM-looking placeholders)
RUN cat << 'EOF' > /home/user/certs_incoming/server_ok.crt
-----BEGIN CERTIFICATE-----
MIIDOk...dummy_ok
-----END CERTIFICATE-----
EOF

RUN cat << 'EOF' > /home/user/certs_incoming/server_soon.crt
-----BEGIN CERTIFICATE-----
MIIDOk...dummy_soon
-----END CERTIFICATE-----
EOF

RUN cat << 'EOF' > /home/user/certs_incoming/server_expired.crt
-----BEGIN CERTIFICATE-----
MIIDOk...dummy_expired
-----END CERTIFICATE-----
EOF

# Permissions
RUN chmod -R a+rX /home/user && \
    chown -R 1000:1000 /home/user || true && \
    rm -rf /home/user/cert_analysis || true

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /home/user

# Runscript equivalent as CMD
CMD ["sh", "-c", "echo 'Container for certificate analysis task.' && echo 'Use docker exec ... to run your commands.'"]