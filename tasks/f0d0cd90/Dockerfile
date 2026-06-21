FROM ubuntu:22.04

# Help/labels
LABEL Author="ChatGPT"
LABEL Description="Container for query-tuning backup task; provides initial state and pytest."

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        tar \
        gzip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/db_scripts && \
    mkdir -p /home/user/backups && \
    mkdir -p /home/user/backup_logs

RUN printf -- "-- Schema definition placeholder\n" > /home/user/db_scripts/schema.sql && \
    printf -- "-- Query optimization placeholder\n" > /home/user/db_scripts/optimize_queries.sql

RUN chmod 755 /home/user/db_scripts && \
    chmod 755 /home/user/db_scripts/schema.sql /home/user/db_scripts/optimize_queries.sql && \
    chmod 777 /home/user/backups /home/user/backup_logs