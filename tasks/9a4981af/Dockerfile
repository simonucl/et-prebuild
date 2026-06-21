FROM ubuntu:22.04

# Author backup-log-task
# Description "Initial state for backup log line–count summary exercise"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip python3-setuptools ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/data/backups && \
    mkdir -p /home/user/data/backup_reports && \
    chmod 755 /home/user/data && \
    chmod 755 /home/user/data/backups && \
    chmod 755 /home/user/data/backup_reports

RUN cat > /home/user/data/backups/2023-05-01.log <<'EOF'
2023-05-01 00:00:01 Backup job started
2023-05-01 00:15:23 Compressing data
2023-05-01 00:45:50 Uploading archive
2023-05-01 01:10:05 Verification successful
2023-05-01 01:10:06 Backup completed
EOF

RUN cat > /home/user/data/backups/2023-05-02.log <<'EOF'
2023-05-02 00:00:02 Backup job started
2023-05-02 00:54:10 Backup failed: network timeout
2023-05-02 00:54:11 Backup aborted
EOF

RUN cat > /home/user/data/backups/2023-05-03.log <<'EOF'
2023-05-03 00:00:02 Backup job started
2023-05-03 00:25:15 Compressing data
2023-05-03 00:49:40 Uploading archive
2023-05-03 01:05:12 Backup completed
EOF

RUN chmod 644 /home/user/data/backups/2023-05-01.log && \
    chmod 644 /home/user/data/backups/2023-05-02.log && \
    chmod 644 /home/user/data/backups/2023-05-03.log

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

CMD echo "Container ready: backup log exercise environment initialized."