# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author chatbot
# Description "Environment for database-backup shell task. Pytest pre-installed."

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

RUN set -eux && \
    if ! id -u user >/dev/null 2>&1; then \
        useradd -m -s /bin/bash user; \
    fi && \
    chmod 755 /home/user && \
    rm -rf /home/user/db_backups || true && \
    rm -f /home/user/backup_setup.log || true && \
    EXPORT_LINE='export BACKUP_DIR="/home/user/db_backups"' && \
    if [ -f /home/user/.bashrc ]; then \
        sed -i "\|${EXPORT_LINE}|d" /home/user/.bashrc; \
    fi

LABEL Author="chatbot"
LABEL Description="Environment for database-backup shell task. Pytest pre-installed."

CMD ["/bin/bash", "-l"]