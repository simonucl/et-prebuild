# Converted from Apptainer definition file
FROM ubuntu:22.04

ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV DEBIAN_FRONTEND=noninteractive

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/db_backups/logs && \
    mkdir -p /home/user/db_backups/reports && \
    chmod 755 /home/user/db_backups/logs && \
    chmod 777 /home/user/db_backups/reports

RUN cat <<'EOF' > /home/user/db_backups/logs/backup_2023-07-08.log
[2023-07-08 03:03:12] INFO  db=customers  status=SUCCESS  duration=43s
[2023-07-08 03:04:01] ERROR db=customers  code=BKUP-013  msg="Could not open backup file"
[2023-07-08 03:05:09] INFO  db=customers  status=END   duration=44s
EOF

RUN cat <<'EOF' > /home/user/db_backups/logs/backup_2023-07-10.log
[2023-07-10 01:00:12] INFO  db=orders  status=START
[2023-07-10 01:01:55] ERROR db=orders  code=BKUP-001  msg="Tablespace read error"
[2023-07-10 01:02:40] INFO  db=orders  status=END duration=99s
EOF

RUN cat <<'EOF' > /home/user/db_backups/logs/backup_2023-07-12.log
[2023-07-12 04:17:07] INFO  db=inventory  status=START
[2023-07-12 04:18:00] WARN  db=inventory  message="Slow I/O detected"
[2023-07-12 04:19:22] ERROR db=inventory  code=BKUP-047  msg="Checksum mismatch"
[2023-07-12 04:20:00] INFO  db=inventory  status=END duration=173s
EOF

RUN cat <<'EOF' > /home/user/db_backups/logs/backup_2023-07-14.log
[2023-07-14 02:55:02] INFO  db=analytics  status=START
[2023-07-14 02:56:34] ERROR db=analytics  code=BKUP-001  msg="Tablespace read error"
[2023-07-14 03:01:10] ERROR db=analytics  code=BKUP-099  msg="Destination full"
[2023-07-14 03:02:00] INFO  db=analytics  status=END duration=355s
EOF

RUN chmod 644 /home/user/db_backups/logs/backup_*.log

CMD ["bash"]