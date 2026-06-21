FROM ubuntu:22.04

# Author youn
# This container provides the initial state for the "database backup
# symlink update" task. It includes:
#   • /home/user/db_backups/ with three zero-byte .sql.gz files
#   • 'latest' symlink pointing to backup_2023-07-02.sql.gz
#   • pytest installed for grading

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
ENV PYTHONUNBUFFERED=1

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/db_backups

RUN touch /home/user/db_backups/backup_2023-07-01.sql.gz && \
    touch /home/user/db_backups/backup_2023-07-02.sql.gz && \
    touch /home/user/db_backups/backup_2023-07-03.sql.gz

RUN ln -sf backup_2023-07-02.sql.gz /home/user/db_backups/latest

RUN chmod 755 /home/user && \
    chmod 755 /home/user/db_backups && \
    chmod 644 /home/user/db_backups/backup_2023-07-*.sql.gz

RUN rm -f /home/user/db_backups/link_update.log