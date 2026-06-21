FROM ubuntu:22.04

# Base system utilities
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        tar \
        gzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Python tooling for the grader
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Directory skeleton
RUN mkdir -p /home/user/envs && \
    mkdir -p /home/user/backup_logs && \
    mkdir -p /home/user/archives

# Create the virtual environment and install required packages
RUN python3 -m venv /home/user/envs/archive_admin && \
    . /home/user/envs/archive_admin/bin/activate && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pandas==2.0.3 requests==2.31.0 && \
    deactivate

# Produce the required requirements.txt
RUN printf 'pandas==2.0.3\nrequests==2.31.0\n' \
    > /home/user/envs/archive_admin/requirements.txt

# Produce the package inventory log
RUN printf 'PACKAGE,VERSION\npandas,2.0.3\nrequests,2.31.0\n' \
    > /home/user/backup_logs/package_inventory.log

# Create the compressed backup archive
# Paths inside the archive must be relative to /home/user
RUN cd /home/user && \
    tar -czf /home/user/archives/pip_backup.tgz \
        envs/archive_admin \
        backup_logs/package_inventory.log

# Set permissive permissions so the non-root runtime user can work
RUN chmod -R a+rX /home/user && \
    chmod -R a+w /home/user/envs /home/user/backup_logs /home/user/archives

# Environment setup
ENV HOME=/home/user

WORKDIR /home/user