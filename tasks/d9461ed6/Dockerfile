FROM ubuntu:22.04

# Labels
LABEL Author="configuration-audit-setup"
LABEL Description="Container prepared for the configuration-file audit assignment"

# Install runtime requirements
RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare directory structure
RUN mkdir -p /home/user/config_backups/old && \
    mkdir -p /home/user/audit && \
    chmod 0777 /home/user/audit

# Populate /home/user/config_backups/sshd.conf
RUN cat > /home/user/config_backups/sshd.conf <<'EOF'
# sshd configuration
Port 22
PermitRootLogin no
PasswordAuthentication yes
ChallengeResponseAuthentication no
EOF

# Populate /home/user/config_backups/nginx.conf
RUN cat > /home/user/config_backups/nginx.conf <<'EOF'
# nginx configuration
user www-data;
worker_processes auto;
pid /run/nginx.pid;
events { worker_connections 768; }
http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
EOF

# Populate /home/user/config_backups/app.conf
RUN cat > /home/user/config_backups/app.conf <<'EOF'
# application configuration
debug=false
port=8080
log_level=info
EOF

# Populate /home/user/config_backups/old/legacy.conf
RUN cat > /home/user/config_backups/old/legacy.conf <<'EOF'
# legacy configuration
feature_x=disabled
safe_mode=true
EOF

# Populate /home/user/config_backups/readme.txt
RUN cat > /home/user/config_backups/readme.txt <<'EOF'
This directory stores configuration backups.
Non-.conf files should be ignored by the audit script.
EOF

# Set permissions - ensure all files are readable by everyone
RUN chmod -R a+r /home/user/config_backups && \
    chmod 755 /home/user

# Environment variables
ENV PYTHONUNBUFFERED=1

# Help information (as comments)
# This container image contains the pre-populated directory tree and files
# required for the "configuration-file audit" task, along with Python and
# pytest for automated grading.