FROM ubuntu:22.04

# Labels
LABEL Author="backup-integrity-setup"
LABEL Description="Environment for backup integrity exercise with pytest pre-installed."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/backup/logs && \
    mkdir -p /home/user/backup/reports

RUN cat > /home/user/backup/logs/backup_2023-09-15.log <<'EOF'
2023-09-15 02:10:34 [INFO] Backup started
2023-09-15 02:12:11 [OK] file: /var/data/db1.sql (checksum=ae34bc...)
2023-09-15 02:12:15 [ERROR] FILE_MISSING /var/data/config.yml
2023-09-15 02:12:16 [OK] file: /var/data/report.pdf (checksum=5b9a7d...)
2023-09-15 02:12:20 [WARNING] CHECKSUM_MISMATCH /var/data/image.png
2023-09-15 02:12:25 [OK] file: /var/data/archive.tar.gz (checksum=9d4e8f...)
2023-09-15 02:12:35 [ERROR] FILE_MISSING /var/data/old_backup.tar.gz
2023-09-15 02:13:10 [INFO] Backup finished: duration=2m36s
EOF

RUN chmod 0755 /home/user && \
    chmod 0755 /home/user/backup && \
    chmod 0755 /home/user/backup/logs && \
    chmod 0777 /home/user/backup/reports && \
    chmod 0644 /home/user/backup/logs/backup_2023-09-15.log

# Run script equivalent (Docker won't execute automatically; kept for reference)
# echo "Container for backup integrity exercise. Open a shell with 'docker run -it <img> /bin/bash'"