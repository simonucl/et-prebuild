FROM ubuntu:22.04

# Help
# This container supplies the initial state for the “backup manifest → CSV” exercise.
# It provides:
# • /home/user/backups/2023-05-10/backup_manifest_20230510.txt
# • pytest for automated grading

RUN set -e && mkdir -p /home/user && chmod 0777 /home/user

RUN BACKUP_DIR="/home/user/backups/2023-05-10" && \
    mkdir -p "${BACKUP_DIR}" && \
    chmod -R 0777 /home/user/backups

RUN cat <<'EOF' > /home/user/backups/2023-05-10/backup_manifest_20230510.txt
# Backup Manifest generated 2023-05-10
/etc/passwd:2048
/etc/group:1024
/var/log/syslog:512000
/home/user/data.txt:4096
/usr/local/bin/script.sh:8192
EOF

RUN chmod 0666 /home/user/backups/2023-05-10/backup_manifest_20230510.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

LABEL Author="backup-admin-scenario"
LABEL Description="Environment for backup manifest conversion task with pytest pre-installed."