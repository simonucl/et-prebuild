FROM ubuntu:22.04

# Help:
# This container provides the initial filesystem state for the
# “backup-and-restore” integrity-check task. pytest is available for
# automated grading.

RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN set -e && \
    if ! getent passwd 1000 >/dev/null 2>&1; then \
        groupadd -g 1000 user || true; \
        useradd -m -u 1000 -g 1000 -s /bin/bash user || true; \
    fi

RUN mkdir -p /home/user/backup

RUN printf 'a' > /home/user/backup/weekly_backup.dat

RUN printf 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb  weekly_backup.dat\n' \
    > /home/user/backup/weekly_backup.sha256

RUN chown -R 1000:1000 /home/user && \
    chmod 0755 /home/user/backup && \
    chmod 0644 /home/user/backup/weekly_backup.dat /home/user/backup/weekly_backup.sha256

RUN chmod 755 /home/user

ENV PATH="$PATH:$HOME/.local/bin"

LABEL Author="Apptainer Task Setup"
LABEL Description="Environment for the backup-and-restore checksum task with pytest pre-installed"