FROM ubuntu:22.04

# Base tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        --no-install-recommends && \
    pip3 install --no-cache-dir pytest

# Prepare initial task data
RUN mkdir -p /home/user/configs && \
    mkdir -p /home/user/changes

RUN cat > /home/user/configs/registration.csv <<'EOF'
server_id;location;role;maint_window
srv01;us-east;web;Sun 01:00
srv02;us-west;db;Mon 02:00
srv03;eu-central;cache;Tue 03:00
EOF

RUN cat > /home/user/changes/firmware_versions.tsv <<'EOF'
server_id	version	release_date
srv01	1.2.4	2024-01-21
srv02	1.4.7	2024-02-10
srv03	1.3.2	2024-02-28
EOF

# Permissions
RUN chmod -R a+rwx /home/user && chmod 755 /home/user

# Environment
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8