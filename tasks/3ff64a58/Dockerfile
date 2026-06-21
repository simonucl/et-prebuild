FROM ubuntu:22.04

# Help:
# This container sets up the starting filesystem conditions for the
# “tidy-up PostgreSQL dump area” exercise and includes pytest for the
# accompanying test suites.

LABEL Author="Container prepared for PostgreSQL symlink tidy-up task" \
      Description="Provides initial state and pytest for automated assessment."

ENV PATH=/usr/local/bin:/usr/bin:/bin

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && \
    ARCHIVES=/home/user/db_archives && \
    mkdir -p "${ARCHIVES}" && \
    touch "${ARCHIVES}/prod_20230918.sql.gz" && \
    touch "${ARCHIVES}/prod_20230919.sql.gz" && \
    touch "${ARCHIVES}/stg_20230918.sql.gz" && \
    touch "${ARCHIVES}/stg_20230919.sql.gz" && \
    BACKUPS=/home/user/db_backups && \
    mkdir -p "${BACKUPS}" && \
    ln -s "${ARCHIVES}/prod_20230918.sql.gz"  "${BACKUPS}/latest_prod" && \
    ln -s "${ARCHIVES}/stg_20230918.sql.gz"   "${BACKUPS}/latest_staging"

RUN chmod 755 /home/user && \
    chmod 755 /home/user/db_archives /home/user/db_backups && \
    chmod 644 /home/user/db_archives/*.sql.gz