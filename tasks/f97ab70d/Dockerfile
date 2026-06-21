FROM ubuntu:22.04

# Help text
# Container for SSL/TLS backup-and-restore exercise. Start an interactive shell:
# exec bash -l

RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/etc/ssl/private && \
    mkdir -p /home/user/etc/ssl/certs

RUN cat > /home/user/etc/ssl/private/server.key <<'EOF'
-----BEGIN KEY-----
foo
-----END KEY-----
EOF

RUN cat > /home/user/etc/ssl/certs/server.crt <<'EOF'
-----BEGIN CERTIFICATE-----
bar
-----END CERTIFICATE-----
EOF

RUN cat > /home/user/etc/ssl/certs/ca.pem <<'EOF'
-----BEGIN CERTIFICATE-----
baz
-----END CERTIFICATE-----
EOF

RUN chmod -R a+rwX /home/user

RUN chmod 755 /home/user

LABEL Author="task-setup"
LABEL Description="Initial state for SSL/TLS backup-and-restore exercise"

CMD echo "Container for SSL/TLS backup-and-restore exercise. Start an interactive shell:" && bash -l