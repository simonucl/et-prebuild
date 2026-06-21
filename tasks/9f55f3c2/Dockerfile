# Converted from Apptainer .def
FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Setup"
LABEL Description="Container image pre-provisioned for the sync automation task with initial directory structure and pytest installed."

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Install packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip rsync --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create directories
RUN mkdir -p /home/user/app_configs && \
    mkdir -p /home/user/remote_host

# Create database.yml
RUN cat <<'EOF' >/home/user/app_configs/database.yml
adapter: postgresql
encoding: utf8
pool: 5
EOF

# Create redis.conf
RUN cat <<'EOF' >/home/user/app_configs/redis.conf
maxmemory 256mb
appendonly yes
EOF

# Create app.env
RUN cat <<'EOF' >/home/user/app_configs/app.env
RAILS_ENV=production
SECRET_KEY_BASE=abc123xyz
EOF

# Set permissions
RUN chmod 644 /home/user/app_configs/database.yml /home/user/app_configs/redis.conf /home/user/app_configs/app.env && \
    chmod 755 /home/user/app_configs && \
    chmod 777 /home/user && \
    chmod 777 /home/user/remote_host