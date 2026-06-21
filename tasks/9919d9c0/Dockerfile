FROM ubuntu:22.04

# Author cloud-migration-task
# Description "Base image for Cloud Migration Cron Job exercise – initial clean state"

ENV PATH=/home/user/.local/bin:$PATH

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y python3 python3-pip cron && \
    useradd -m -s /bin/bash user && \
    rm -rf /home/user/bin /home/user/logs /home/user/reports /home/user/migration || true && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

LABEL Author="cloud-migration-task" \
      Description="Base image for Cloud Migration Cron Job exercise – initial clean state"