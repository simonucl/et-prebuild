FROM ubuntu:22.04

# Help text (from %help / %runscript)
# Container for restore-test. Run your commands or open a shell.

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tar \
        gzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN set -e && \
    BACKUP_BASE="/home/user/backup_server/home_snapshots" && \
    TMP_BUILD="/tmp/projectA" && \
    mkdir -p "${BACKUP_BASE}" && \
    mkdir -p "${TMP_BUILD}" && \
    chmod 755 /home /home/user /home/user/backup_server "${BACKUP_BASE}" && \
    printf "Alpha\n" > "${TMP_BUILD}/file1.txt" && \
    printf "Beta\n"  > "${TMP_BUILD}/file2.txt" && \
    printf "# Project A Notes\nRestored successfully.\n" > "${TMP_BUILD}/notes.md" && \
    tar -C /tmp -czf "${BACKUP_BASE}/projectA_2023-08-01.tar.gz" projectA && \
    chmod 644 "${BACKUP_BASE}/projectA_2023-08-01.tar.gz" && \
    rm -rf "${TMP_BUILD}"

LABEL Author="restore-task-preparer"
LABEL Description="Environment for restore test – contains backup snapshot and pytest"