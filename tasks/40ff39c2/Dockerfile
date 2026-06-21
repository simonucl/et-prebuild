# Converted from Apptainer definition file
FROM ubuntu:22.04

# %help section
# This container prepares the initial state for the “backup-restore” exercise.
# It installs pytest and provides the backup archive at:
# /home/user/backup_repo/system_backup_2023-10-05.tar.gz

ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    echo "=== Updating apt and installing Python & pytest ===" && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip tar && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/backup_repo && \
    chmod 755 /home/user && \
    chmod 755 /home/user/backup_repo && \
    mkdir -p /tmp/backup_build/etc/ssh && \
    mkdir -p /tmp/backup_build/var/log

RUN cat > /tmp/backup_build/etc/hostname <<'EOF'
backup-test-host
EOF

RUN cat > /tmp/backup_build/etc/ssh/sshd_config <<'EOF'
# SSH Daemon Config for testing
Port 2222
PermitRootLogin no
PasswordAuthentication yes
EOF

RUN cat > /tmp/backup_build/var/log/test.log <<'EOF'
This is a test log for restore validation.
EOF

RUN tar -C /tmp/backup_build -czf /home/user/backup_repo/system_backup_2023-10-05.tar.gz etc var && \
    chmod 644 /home/user/backup_repo/system_backup_2023-10-05.tar.gz && \
    rm -rf /tmp/backup_build

LABEL Author="Container Build Script"
LABEL Description="Environment for backup-restore task with pytest pre-installed."