# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directory tree
RUN mkdir -p /home/user/configs

# httpd.conf
RUN cat <<'EOF' > /home/user/configs/httpd.conf
ServerRoot /etc/httpd
Listen 80
EOF

# nginx.conf
RUN cat <<'EOF' > /home/user/configs/nginx.conf
worker_processes  1;
error_log  /var/log/nginx/error.log;
EOF

# ssh.conf
RUN cat <<'EOF' > /home/user/configs/ssh.conf
Port 22
PermitRootLogin no
EOF

# Permissions
RUN chmod -R 777 /home/user

# Environment variables
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Additional chmod from environment section
RUN chmod 755 /home/user

CMD ["bash"]