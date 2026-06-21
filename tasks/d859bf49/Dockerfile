FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem layout for the task
# Base working directory for the non-root user expected by the tests
RUN mkdir -p /home/user

# 1. Source data that must be archived later
RUN mkdir -p /home/user/data_to_backup/docs && \
    mkdir -p /home/user/data_to_backup/images && \
    mkdir -p /home/user/data_to_backup/scripts

# docs/report.txt
RUN printf 'Quarterly\n' > /home/user/data_to_backup/docs/report.txt

# images/photo*.jpg (dummy JPEG markers with LF)
RUN printf 'JPEG_DUMMY_DATA_1\n' > /home/user/data_to_backup/images/photo1.jpg && \
    printf 'JPEG_DUMMY_DATA_2\n' > /home/user/data_to_backup/images/photo2.jpg

# scripts/cleanup.sh
RUN printf '#!/bin/bash\n' > /home/user/data_to_backup/scripts/cleanup.sh && \
    printf 'echo cleanup\n' >> /home/user/data_to_backup/scripts/cleanup.sh && \
    chmod +x /home/user/data_to_backup/scripts/cleanup.sh

# 2. "Remote host" directory – must start out empty
RUN mkdir -p /home/user/remote_host

# Permissions: ensure the runtime unprivileged user can write
RUN chmod -R a+rX /home/user && \
    chmod 777 /home/user && \
    chmod 777 /home/user/remote_host && \
    chown -R 1000:1000 /home/user || true

# Environment variables
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:$PATH