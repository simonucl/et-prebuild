# Author: OpenAI Assistant
# Description: Apptainer image for backup operator task with initial config files and pytest installed.

FROM ubuntu:22.04

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest PyYAML toml && \
    mkdir -p /home/user/backup

RUN cat <<'EOF' > /home/user/backup/config.yml
version: "1.0"
jobs:
  daily_backup:
    enabled: true
    source: /data
    destination: /backups/daily
    retention_days: 7
  restore_test:
    enabled: false
    source: /backups/daily/latest
    destination: /tmp/restore_test
    retention_days: 1
EOF

RUN cat <<'EOF' > /home/user/backup/job.toml
[general]
log_level = "INFO"
threads = 2

[job.daily_backup]
cron = "0 2 * * *"
compression = "gzip"

[job.restore_test]
cron = ""
compression = "none"
EOF

RUN chmod 0644 /home/user/backup/config.yml /home/user/backup/job.toml && \
    chmod 0755 /home/user /home/user/backup && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH