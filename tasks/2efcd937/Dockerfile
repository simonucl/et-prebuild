FROM ubuntu:22.04

LABEL Author="backup-integrity-setup"
LABEL Description="Initial state for backup-integrity engineer task"

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir --upgrade pip pytest

RUN mkdir -p /home/user/backup/raw

RUN cat > /home/user/backup/raw/file_checksums.csv <<'EOF'
abc123 /backups/2023-09-01/home/user/docs/report.docx
def456 /backups/2023-09-01/home/user/docs/budget.xlsx
ghi789 /backups/2023-09-01/home/user/docs/plan.pdf
abc123 /backups/2023-10-01/home/user/docs/report.docx
def456 /backups/2023-10-01/home/user/docs/budget.xlsx
jkl012 /backups/2023-10-01/home/user/docs/meeting_minutes.docx
mno345 /backups/2023-11-01/home/user/docs/notes.txt
abc123 /backups/2023-11-01/home/user/docs/report.docx
def456 /backups/2023-11-01/home/user/docs/budget.xlsx
xyz999 /backups/2023-11-01/home/user/docs/image.png
EOF

RUN chmod 755 /home/user /home/user/backup /home/user/backup/raw && \
    chmod 644 /home/user/backup/raw/file_checksums.csv