# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ---------------------------------------------------------------------
# Install Python tooling and pytest
# ---------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------
# Create user and home directory
# ---------------------------------------------------------------------
RUN set -e && \
    useradd -m -d /home/user user && \
    chmod 755 /home/user

# ---------------------------------------------------------------------
# Seed the backup log required by the exercise
# ---------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user/backup/logs

RUN cat <<'EOF' > /home/user/backup/logs/backup_20230815.log
[2023-08-15 00:01:02] INFO  Starting backup job id=42
[2023-08-15 00:01:05] INFO  Scanning files to backup
[2023-08-15 00:03:12] WARN  File /var/data/tmp/cache.dat skipped (permission denied)
[2023-08-15 00:05:55] ERROR Unable to open /var/data/important.db (I/O error)
[2023-08-15 00:06:10] INFO  Retrying missing files
[2023-08-15 00:07:25] WARN  Checksum mismatch ignored for /var/data/old.log
[2023-08-15 00:08:30] ERROR Failed to write to backup destination (disk full)
[2023-08-15 00:10:00] INFO  Backup job ended
EOF

RUN chmod 644 /home/user/backup/logs/backup_20230815.log && \
    chown -R user:user /home/user

LABEL Author="backup-integrity-exercise"