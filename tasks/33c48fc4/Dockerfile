FROM ubuntu:22.04

# Help / labels
# Author: ChatGPT
# Description: Initial state for the backup-integrity exercise with pytest pre-installed.
LABEL Author="ChatGPT"
LABEL Description="Initial state for the backup-integrity exercise with pytest pre-installed."

RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip python3-setuptools python3-venv \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN set -eux && \
    if ! id -u 1000 >/dev/null 2>&1; then \
        adduser --disabled-password --gecos "" --uid 1000 user; \
    fi

RUN set -eux && \
    mkdir -p /home/user/backups/daily && \
    mkdir -p /home/user/backups/weekly && \
    printf 'abc' > /home/user/backups/daily/db.sql.gz && \
    printf 'abc' > /home/user/backups/daily/files.tar.gz && \
    printf 'def' > /home/user/backups/weekly/full.tar.gz

RUN cat <<'EOF' > /home/user/backups/reference-manifest.log
daily/db.sql.gz|3|ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
daily/files.tar.gz|3|ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
weekly/full.tar.gz|3|ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
EOF

RUN echo >> /home/user/backups/reference-manifest.log

RUN set -eux && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/backups && \
    chmod 0755 /home/user/backups/daily && \
    chmod 0755 /home/user/backups/weekly && \
    chmod 0644 /home/user/backups/daily/db.sql.gz && \
    chmod 0644 /home/user/backups/daily/files.tar.gz && \
    chmod 0644 /home/user/backups/weekly/full.tar.gz && \
    chmod 0644 /home/user/backups/reference-manifest.log && \
    chown -R 1000:1000 /home/user

# Environment
ENV PATH="/home/user/.local/bin:${PATH}"