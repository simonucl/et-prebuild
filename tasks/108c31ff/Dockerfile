FROM ubuntu:22.04

# Help text
# This container image sets up the initial filesystem state required for the
# “quick security-hygiene scan on PostgreSQL backups” assignment. It contains:
#   • /home/user/db_backups/ with three sample backup files
#   • pytest (via pip) for the automated test harness

LABEL Author="quickscan-builder"
LABEL Description="Base image for PostgreSQL backup security-hygiene assignment. Seeds three backup files in /home/user/db_backups and installs pytest."

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip gzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/db_backups

RUN cat >/home/user/db_backups/hr_2023-05-01.sql <<'EOF'
-- HR Database dump
CREATE TABLE employees(id int);
CREATE ROLE hr_user WITH LOGIN PASSWORD 'secret123';
-- End
EOF

RUN chmod 0644 /home/user/db_backups/hr_2023-05-01.sql

RUN cat >/home/user/db_backups/dev_2023-05-01.sql <<'EOF'
-- Dev DB
SELECT 1;
EOF

RUN chmod 0600 /home/user/db_backups/dev_2023-05-01.sql

RUN echo "Dummy sales backup" | gzip -c >/home/user/db_backups/sales_2023-05-01.sql.gz

RUN chmod 0600 /home/user/db_backups/sales_2023-05-01.sql.gz

RUN chmod 755 /home/user

ENV HOME=/home/user