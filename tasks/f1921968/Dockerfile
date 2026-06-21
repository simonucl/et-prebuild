FROM ubuntu:22.04

# Help:
# This container sets up the initial state for the “database backup” task.
# It provides /home/user/backup.sh (not executable) and no further artefacts.
# Pytest is pre-installed so that the automated checker can validate both the
# initial and final states.

LABEL Author="database-backup exercise scaffold"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user

RUN cat >/home/user/backup.sh <<'EOF'
#!/bin/bash
echo "backup executed"
EOF

RUN chmod 0644 /home/user/backup.sh && \
    chown 1000:1000 /home/user/backup.sh && \
    chown 1000:1000 /home/user && \
    chmod 0755 /home/user