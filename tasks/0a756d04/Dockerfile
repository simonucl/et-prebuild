FROM ubuntu:22.04

# Author "Apptainer Build Script for Backup Manifest Task"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/backup

RUN chmod 0777 /home/user/backup

RUN cat > /home/user/backup/files_to_backup.txt <<'EOF'
/etc/hosts
/home/user/data/report1.csv
/etc/hosts
/var/log/syslog
/home/user/data/report2.csv
/var/log/syslog
EOF

RUN chmod 0666 /home/user/backup/files_to_backup.txt

RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:$PATH"