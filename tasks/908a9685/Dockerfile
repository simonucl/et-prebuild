FROM ubuntu:22.04

# Install Python, pip, and dependencies
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Prepare filesystem state
RUN mkdir -p /home/user/backups/daily && \
    mkdir -p /home/user/backup_reports

# Create backup files with exact content
RUN printf "[main]\nkey=value\n" > /home/user/backups/daily/config_backup.conf
RUN printf "CREATE TABLE test(id INT);\n" > /home/user/backups/daily/db_dump.sql
RUN printf "dummy tar content\n" > /home/user/backups/daily/site_files.tar.gz

# Set permissions
RUN chmod 755 /home/user /home/user/backups /home/user/backups/daily /home/user/backup_reports && \
    chmod 644 /home/user/backups/daily/*

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Default runscript equivalent
CMD echo "This container is prepared for the backup-integrity spot-check exercise." && \
    echo "Run the provided tasks or open a shell to begin."