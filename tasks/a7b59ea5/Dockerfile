# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text
# This Apptainer image contains all files necessary for the “backup-operator”
# exercise. The backup script, cron entry, systemd service and timer units,
# as well as an initial backup and log entry, are pre-created in /home/user.

LABEL Author="backup-operator-preparation"
LABEL Description="Container prepared for backup script exercise with cron and systemd unit files."

ENV PATH="/home/user/backup_scripts:${PATH}"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/backup_test/source && \
    mkdir -p /home/user/backup_test/backup && \
    mkdir -p /home/user/backup_scripts && \
    mkdir -p /home/user/.config/systemd/user

RUN printf 'Important data v1\n' > /home/user/backup_test/source/important.txt

RUN cat << 'EOF' > /home/user/backup_scripts/backup_once.sh
#!/bin/sh
SRC="/home/user/backup_test/source/important.txt"
DST="/home/user/backup_test/backup/important.txt"
LOG="/home/user/backup_scripts/backup.log"

# Ensure the destination directory exists
mkdir -p "$(dirname "$DST")"

# Copy the file (overwrite if it already exists)
cp "$SRC" "$DST"

# Append ISO-8601 timestamped log entry
date --iso-8601=seconds | awk '{printf "%s : Backed up important.txt\n", $0}' >> "$LOG"
    chmod 755 /home/user

EOF

RUN chmod 0755 /home/user/backup_scripts/backup_once.sh

RUN /home/user/backup_scripts/backup_once.sh

RUN printf '17 2 * * * /home/user/backup_scripts/backup_once.sh\n' > /home/user/backup_scripts/backup.cron

RUN cat << 'EOF' > /home/user/.config/systemd/user/backup_once.service
[Unit]
Description=One-off user backup

[Service]
Type=oneshot
ExecStart=/home/user/backup_scripts/backup_once.sh
EOF

RUN cat << 'EOF' > /home/user/.config/systemd/user/backup_once.timer
[Unit]
Description=Run user backup 5 minutes after boot

[Timer]
OnBootSec=5min
Unit=backup_once.service

[Install]
WantedBy=default.target
EOF

RUN chmod -R a+rX /home/user/backup_test && \
    chmod -R a+rX /home/user/backup_scripts && \
    chmod 0700 /home/user/.config && \
    chmod -R a+rX /home/user/.config/systemd && \
    chmod 0700 /home/user/.config/systemd/user