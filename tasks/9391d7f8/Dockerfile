FROM ubuntu:22.04

# Author: backup-permissions-exercise
# Description: Environment for the database-backup permission hardening task

ENV PYTHONUNBUFFERED=1

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/db_backups && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/db_backups && \
    echo "TESTDATA" > /home/user/db_backups/production.db && \
    chmod 0664 /home/user/db_backups/production.db

RUN chmod 755 /home/user