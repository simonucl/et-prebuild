# Based on Apptainer: Bootstrap localimage / From: ./ubuntu_22.04.sif
# Using closest Docker equivalent
FROM ubuntu:22.04

# Help text from %help (not provided; using runscript text)
# Container for PostgreSQL backup-archiving exercise.
# Run your commands inside an interactive shell:
#     apptainer exec <container.sif> /bin/bash

ENV PYTHONIOENCODING=UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-venv \
        ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 0777 /home/user

RUN mkdir -p /home/user/db_backups && chmod 0755 /home/user/db_backups

RUN cat <<'EOF' >/home/user/db_backups/backup_20220115.sql
-- dummy SQL dump for 15 Jan 2022
EOF

RUN cat <<'EOF' >/home/user/db_backups/backup_20220120.sql
-- dummy SQL dump for 20 Jan 2022
EOF

RUN cat <<'EOF' >/home/user/db_backups/backup_20220201.sql
-- dummy SQL dump for 01 Feb 2022
EOF

RUN cat <<'EOF' >/home/user/db_backups/backup_20220210.sql
-- dummy SQL dump for 10 Feb 2022
EOF

RUN chmod 0644 /home/user/db_backups/backup_*.sql && \
    chmod 755 /home/user