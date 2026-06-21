# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python tooling and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create initial filesystem state expected by the tests
RUN mkdir -p /home/user/db_backup

RUN cat > /home/user/db_backup/backup_config.yaml <<'EOF'
schedule:
  frequency: daily
  window: "00:00-06:00"
  compression: false
database:
  host: localhost
  port: 5432
EOF

RUN cat > /home/user/db_backup/storage.conf.toml <<'EOF'
storage_mode = "s3"
bucket = "prod-backups"
retention_days = 7

[network]
timeout_secs = 30
EOF

# Make sure any runtime user can read/write the task files
RUN chmod -R a+rwX /home/user

# Ensure expected permissions
RUN chmod 755 /home/user

LABEL Author="Container preparation script" \
      Description="Sets up initial state for the database-reliability engineer task (pytest included)"