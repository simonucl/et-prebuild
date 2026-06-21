# Converted from Apptainer definition file
FROM ubuntu:22.04

# Basic build utilities and Python tooling
RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        tar \
        gzip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state
RUN mkdir -p /home/user/backups/daily && \
    mkdir -p /home/user/archives && \
    mkdir -p /home/user/backup_logs && \
    echo "-- users data dump"    > /home/user/backups/daily/users.sql && \
    echo "-- orders data dump"   > /home/user/backups/daily/orders.sql && \
    echo "-- products data dump" > /home/user/backups/daily/products.sql && \
    chmod -R 0777 /home/user

# Apply environment permission fix from %environment
RUN chmod 755 /home/user

# Environment variables from %environment
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin