FROM ubuntu:22.04

# Help section
# This Apptainer image provides the starting filesystem state for the
# "backup consolidation" exercise. Three daily log files are present in
# /home/user/backups/daily/. The /home/user/backups/summary/ directory is
# intentionally NOT created. Pytest is installed for automated grading.

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/backups/daily && \
    chmod 755 /home/user && \
    chmod 777 /home/user/backups && \
    chmod 755 /home/user/backups/daily

RUN cat > /home/user/backups/daily/backup_report_2023-08-01.log << 'EOF'
db.sql 20480 9f8b1e2d 2023-08-01
home.tar 512000 c3d8fab1 2023-08-01
etc.cfg 120 1a2b3c4d 2023-08-01
EOF

RUN cat > /home/user/backups/daily/backup_report_2023-08-02.log << 'EOF'
db.sql 20560 af4c9d11 2023-08-02
home.tar 513024 0ddce8ef 2023-08-02
etc.cfg 125 ee44aa55 2023-08-02
EOF

RUN cat > /home/user/backups/daily/backup_report_2023-08-03.log << 'EOF'
db.sql 20640 bb88cc77 2023-08-03
home.tar 514048 2376abdc 2023-08-03
etc.cfg 130 ddd77711 2023-08-03
EOF

RUN chmod 644 /home/user/backups/daily/backup_report_2023-08-*.log

# Labels
LABEL Author="Backup-Training-Setup"
LABEL Description="Environment for backup consolidation task with initial daily logs."