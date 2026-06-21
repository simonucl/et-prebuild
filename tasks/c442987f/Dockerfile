FROM ubuntu:22.04

# Labels
LABEL Author="OpenAI ChatGPT"
LABEL Description="Docker image pre-configured for the credential rotation challenge."

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip rsync ca-certificates && \
    pip3 install --no-cache-dir pytest

# Create home hierarchy
RUN mkdir -p /home/user

# 1. Source directory with credential files
RUN mkdir -p /home/user/secure_configs

RUN cat > /home/user/secure_configs/secret.conf <<'EOF'
DB_PASSWORD=oldpassword
API_KEY=123abc
EOF

RUN cat > /home/user/secure_configs/vault.conf <<'EOF'
TOKEN=abcdef
ROTATION_DATE=2023-09-09
EOF

# 2. Empty destination directory (must be writable later)
RUN mkdir -p /home/user/remote_backup

# 3. Log directory (log file intentionally NOT created)
RUN mkdir -p /home/user/rotation_logs

# Permissions
RUN chmod 0755 /home/user && \
    chmod 0755 /home/user/secure_configs && \
    chmod 0777 /home/user/remote_backup && \
    chmod 0777 /home/user/rotation_logs && \
    chmod 0644 /home/user/secure_configs/*.conf

# Clean up APT caches to keep image small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LANG=C
ENV LC_ALL=C