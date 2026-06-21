FROM ubuntu:22.04

# Basic tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Ensure /home/user exists
RUN mkdir -p /home/user && chmod 755 /home/user

# Create logs directory
RUN mkdir -p /home/user/logs && chmod 755 /home/user/logs

# Create restore.log with exact content
RUN cat > /home/user/logs/restore.log <<'EOF'
2023-09-10 12:45:27 | INFO  | Restore started for backup set ID=BK20230910A
2023-09-10 12:46:00 | WARN  | Missing incremental file inc-20230909-02.delta
2023-09-10 12:46:05 | INFO  | Attempting partial restore
2023-09-10 12:47:10 | ERROR | Restore failed with code ERR42
2023-09-10 12:47:45 | INFO  | Clean-up finished
2023-09-11 08:10:32 | INFO  | Restore started for backup set ID=BK20230911A
2023-09-11 08:10:55 | WARN  | File changed during restore: /var/lib/data/app.db
2023-09-11 08:12:23 | ERROR | Restore aborted due to checksum mismatch
2023-09-11 08:13:00 | INFO  | Sending failure report email
EOF

# Set permissions on the log file
RUN chmod 644 /home/user/logs/restore.log

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

CMD echo "Container for 'restore log alert view' task. Open a shell to work on the exercise."