FROM ubuntu:22.04

# Help text
# This Apptainer image sets up the initial environment for the
# backup-configuration editing exercise. Pytest is included so the
# verification suite can run.

LABEL Author="example"
LABEL Description="Container for PostgreSQL backup-configuration editing task"

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/db_backup

RUN cat >/home/user/db_backup/config.yaml <<'EOF'
version: "2.0"
retention_days: 7
compression: "lz4"
backup_type: "full"
encryption: "aes128"
EOF

RUN cat >/home/user/db_backup/settings.toml <<'EOF'
# Application-level settings
[app]
name = "pg-backup-agent"
version = "1.2.3"

# Storage backend
[storage]
provider = "gcs"
region   = "us-central1"
bucket   = "dev-backups"

# Databases being backed up
[[databases]]
name     = "test"
host     = "test.db.internal"
port     = 5432
EOF

RUN chmod -R 777 /home/user/db_backup

RUN chmod 755 /home/user