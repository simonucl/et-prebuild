FROM ubuntu:22.04

# Help:
# This container sets up the initial environment for the “backup web-server” task.
# It pre-creates:
#   /home/user/db_backups/
#   /home/user/db_backups/backup_2023_09_01.sql  (content: 'SELECT 1;')
# pytest is installed for the automated grading suite.

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/db_backups

RUN cat >/home/user/db_backups/backup_2023_09_01.sql <<'EOF'
SELECT 1;
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/db_backups && \
    chmod 644 /home/user/db_backups/backup_2023_09_01.sql

# Equivalent of %runscript (informational only)
# echo "Container for the backup web-server exercise."
# echo "Use an interactive shell to proceed: apptainer exec <image>.sif /bin/bash"