# Container pre-loaded with backup logs for the “backup-integrity engineer” exercise.
# Includes pytest for automated evaluation.

FROM ubuntu:22.04

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates \
        bash \
        coreutils && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -s /bin/bash user && \
    mkdir -p /home/user/backups/2023-08-01 \
             /home/user/backups/2023-08-02 \
             /home/user/backups/2023-08-03

RUN cat > /home/user/backups/2023-08-01/backup_20230801.log <<'EOF'
2023-08-01 00:59:59 INFO Starting backup
2023-08-01 01:15:42 ERROR db01.tar.gz checksum mismatch
2023-08-01 01:22:10 INFO db01.tar.gz uploaded
2023-08-01 01:30:00 INFO Backup finished
EOF

RUN cat > /home/user/backups/2023-08-02/backup_20230802.log <<'EOF'
2023-08-02 00:59:58 INFO Starting backup
2023-08-02 01:12:02 ERROR web_assets.zip checksum mismatch
2023-08-02 01:12:03 WARN Retrying web_assets.zip upload
2023-08-02 01:44:22 ERROR db02.tar.gz checksum mismatch
2023-08-02 02:01:00 INFO Backup finished
EOF

RUN cat > /home/user/backups/2023-08-03/backup_20230803.log <<'EOF'
2023-08-03 01:00:01 INFO Starting backup
2023-08-03 01:33:47 INFO No errors detected
2023-08-03 02:00:00 INFO Backup finished
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/backups && \
    chmod 755 /home/user/backups/2023-08-01 /home/user/backups/2023-08-02 /home/user/backups/2023-08-03 && \
    chmod 644 /home/user/backups/2023-08-01/backup_20230801.log && \
    chmod 644 /home/user/backups/2023-08-02/backup_20230802.log && \
    chmod 644 /home/user/backups/2023-08-03/backup_20230803.log && \
    chown -R user:user /home/user

ENV HOME=/home/user