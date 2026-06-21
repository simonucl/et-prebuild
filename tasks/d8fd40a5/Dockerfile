FROM ubuntu:22.04

# Labels
LABEL Maintainer="apptainer-setup"

# Update package list and install Python + pip
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Ensure /home/user exists and is writable by any runtime UID
RUN mkdir -p /home/user && \
    chmod 777 /home/user

# Create the directory that will hold the INI configuration
RUN mkdir -p /home/user/db_configs && \
    chmod 755 /home/user/db_configs

# Create the INI file with exact required contents (final newline included)
RUN cat > /home/user/db_configs/db_service.ini <<'EOF'
[database]
host=localhost
port=5432
dbname=inventory
user=inventory_admin

[optimizations]
max_connections=200
work_mem=4MB
shared_buffers=128MB
effective_cache_size=512MB
EOF

RUN chmod 644 /home/user/db_configs/db_service.ini