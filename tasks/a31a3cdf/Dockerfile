FROM ubuntu:22.04

# Update package lists and install Python and pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create required directories and CSV file for the initial state
RUN mkdir -p /home/user/backups

RUN cat >/home/user/backups/backup_report.csv <<'EOF'
BackupID,Date,Status,SizeMB
BKP001,2023-07-01,OK,512
BKP002,2023-07-02,OK,514
BKP003,2023-07-03,FAILED,0
BKP004,2023-07-04,OK,518
BKP005,2023-07-05,OK,520
EOF

# Ensure correct permissions
RUN chmod 777 /home/user/backups && \
    chmod 644 /home/user/backups/backup_report.csv && \
    chmod 755 /home/user

# Environment variables
ENV PYTHONUNBUFFERED=1