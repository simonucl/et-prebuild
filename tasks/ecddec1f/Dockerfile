FROM ubuntu:22.04

# Help / metadata
LABEL Author="OpenAI ChatGPT"
LABEL Description="Container for PostgreSQL backup auditing task – initial state only."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -s /bin/bash user && \
    mkdir -p /home/user/db_backup

RUN cat <<'EOF' > /home/user/db_backup/db_backup.ini
[database]
host = localhost
port = 5432
name = prod_db
user = backup_user

[backup]
backup_dir = /home/user/db_backup/archives
compression = true
method = pg_dump

[retention]
retention_days = 30
EOF

RUN chown -R user:user /home/user/db_backup && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH