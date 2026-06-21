FROM ubuntu:22.04

# Labels
LABEL Author="Security Engineering Task – Credential Rotation"

# Install packages and create user
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    if ! id -u user >/dev/null 2>&1; then \
        useradd -m -u 1000 -s /bin/bash user; \
    fi && \
    mkdir -p /home/user/app/config && \
    mkdir -p /home/user/rotate && \
    mkdir -p /home/user/security

# Initial production database configuration
RUN cat > /home/user/app/config/database.ini <<'EOF'
[database]
user = appuser
password = OldPassw0rd!
host = 127.0.0.1
port = 5432
EOF

# New password to be rotated in
RUN cat > /home/user/rotate/new_pass.txt <<'EOF'
N3wP@ssw0rd-2024!
EOF

# Set ownership and permissions
RUN chown -R user:user /home/user && \
    chmod 755 /home/user && \
    chmod 755 /home/user/app /home/user/app/config && \
    chmod 755 /home/user/rotate && \
    chmod 755 /home/user/security

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin