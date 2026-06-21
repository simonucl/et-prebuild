# Converted from Apptainer definition file
FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directory hierarchy
RUN mkdir -p /home/user/backups/conf && \
    chmod 755 /home/user/backups/conf && \
    chmod 755 /home/user && \
    mkdir -p /home/user/backups && \
    chmod 755 /home/user/backups

# Write db_backup.ini
RUN cat > /home/user/backups/conf/db_backup.ini <<'EOF'
[schedule]
daily_time = 02:30
weekly_day = Sun
weekly_time = 03:00
EOF

RUN chmod 644 /home/user/backups/conf/db_backup.ini

# Environment variables
ENV PATH="$PATH:~/.local/bin"

# Labels
LABEL Author="task-prep"
LABEL Description="Environment for backup scheduler task with pytest installed"

# Default run command
CMD ["echo", "Container for backup scheduler task. Use 'docker run' or 'docker exec' to run commands."]