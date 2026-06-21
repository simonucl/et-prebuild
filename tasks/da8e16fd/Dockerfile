FROM ubuntu:22.04

# Author backup-task-preparer
# Description "Environment for backup integrity verification exercise."

# This container sets up the initial filesystem state for the
# "backup integrity check" task and includes pytest for automated grading.

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare the initial backup directory structure and files
RUN mkdir -p /home/user/backups/daily && \
    touch /home/user/backups/daily/sample.db && \
    printf 'd41d8cd98f00b204e9800998ecf8427e  sample.db\n' > /home/user/backups/daily/sample.db.md5

# Make /home/user writable for the unprivileged runtime user
RUN mkdir -p /home/user && \
    chmod 0777 /home/user