FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest

# Create user and group with UID/GID 1000 (matching the host's non-root user)
RUN groupadd -g 1000 user || true && \
    useradd -m -u 1000 -g 1000 user || true

# Directory structure
RUN mkdir -p /home/user/projects/configs && \
    mkdir -p /home/user/backups

# Set required permissions (0755)
RUN chmod 0755 /home/user/projects && \
    chmod 0755 /home/user/projects/configs && \
    chmod 0755 /home/user/backups

# Populate configuration files with exact content
RUN cat > /home/user/projects/configs/httpd.conf <<'EOF'
# Apache HTTPD configuration
ServerName localhost
Listen 80
EOF

RUN cat > /home/user/projects/configs/sshd.conf <<'EOF'
# OpenSSH daemon configuration
Port 22
PermitRootLogin no
EOF

RUN cat > /home/user/projects/configs/database.conf <<'EOF'
# Example DB configuration
host=127.0.0.1
port=5432
EOF

RUN cat > /home/user/projects/configs/app.conf <<'EOF'
# Application configuration
debug=true
workers=4
EOF

# Ensure deterministic modification times for reproducible archives
RUN touch -t 202001010000 /home/user/projects/configs/*.conf

# Make sure the runtime user can write to /home/user/* paths
RUN chown -R 1000:1000 /home/user

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Default command
CMD ["bash"]