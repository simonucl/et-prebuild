FROM ubuntu:22.04

# Basic utilities and Python tooling
RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        lsof \
        curl \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Create the dedicated user with UID/GID 1000
RUN useradd -m -u 1000 -s /bin/bash user

# Prepare initial filesystem state
RUN mkdir -p /home/user/backups && \
    touch /home/user/backups/full_2024_03_25.sql && \
    touch /home/user/backups/incremental_2024_03_26.sql.gz && \
    mkdir -p /home/user/backup_server && \
    chown -R 1000:1000 /home/user && \
    chmod 0755 /home/user/backups && \
    chmod 0755 /home/user/backup_server && \
    chmod 0644 /home/user/backups/full_2024_03_25.sql && \
    chmod 0644 /home/user/backups/incremental_2024_03_26.sql.gz

# Environment setup
RUN chmod 755 /home/user
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8