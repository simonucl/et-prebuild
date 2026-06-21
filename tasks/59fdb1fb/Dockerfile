# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Basic packages
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        patch \
        diffutils \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Python tooling for the exercise
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Create the dedicated non-privileged user (uid/gid 1000)
# ------------------------------------------------------------------
RUN groupadd -g 1000 user && \
    useradd -u 1000 -g 1000 -s /bin/bash -m -d /home/user user

# ------------------------------------------------------------------
# Populate the baseline and secure template files
# ------------------------------------------------------------------
RUN install -d -m 0755 /home/user/baseline_configs && \
    install -d -m 0755 /home/user/secure_templates

# Baseline (insecure) nginx.conf
RUN cat > /home/user/baseline_configs/nginx.conf <<'EOF'
worker_processes  1;
events {
    worker_connections  1024;
}

http {
    server_tokens on;
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
}
EOF

# Secure (hardened) nginx.conf
RUN cat > /home/user/secure_templates/nginx.conf <<'EOF'
worker_processes  auto;
events {
    worker_connections  2048;
}

http {
    server_tokens off;
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  30;
    add_header X-Content-Type-Options nosniff;
}
EOF

# ------------------------------------------------------------------
# Set ownership and permissions (umask 022 style)
# ------------------------------------------------------------------
RUN chown -R 1000:1000 /home/user && \
    find /home/user -type d -exec chmod 0755 {} + && \
    find /home/user -type f -exec chmod 0644 {} + && \
    chmod 755 /home/user

# ------------------------------------------------------------------
# Environment variables
# ------------------------------------------------------------------
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV HOME=/home/user

# ------------------------------------------------------------------
# Labels
# ------------------------------------------------------------------
LABEL Author="devsecops-task-preparer" \
      Description="Environment for Nginx compliance patch exercise with pytest pre-installed."

USER user
WORKDIR /home/user

CMD ["bash"]