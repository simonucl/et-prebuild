# syntax=docker/dockerfile:1
# Converted from Apptainer definition using ubuntu:22.04 as base
FROM ubuntu:22.04

# Help text
# This container sets up the initial filesystem and tools
# needed for the “legacy service hardening” exercise.

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create required directory structure
RUN mkdir -p /home/user/legacy_services/hardened && \
    mkdir -p /home/user/hardening

# Populate legacy configuration files
RUN cat > /home/user/legacy_services/nginx.conf.old <<'EOF'
user www-data;
worker_processes auto;
server_tokens on;
ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
EOF

RUN cat > /home/user/legacy_services/sshd_config.old <<'EOF'
# SSH Daemon Configuration
PermitRootLogin yes
PasswordAuthentication yes
EOF

RUN cat > /home/user/legacy_services/httpd.conf.old <<'EOF'
# Apache HTTPD Configuration
ServerSignature On
TraceEnable On
EOF

# Ensure correct permissions
RUN chmod -R u+rwX,go+rX /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Labels
LABEL Author="hardening-task"
LABEL Description="Initial state for legacy service hardening exercise"