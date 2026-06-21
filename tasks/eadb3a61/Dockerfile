FROM ubuntu:22.04

# Set environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONIOENCODING=utf-8

# Install Python + pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state for the exercise
# Base directories
RUN mkdir -p /home/user/backup/logs && \
    mkdir -p /home/user/backup/verification && \
    chmod 755 /home/user && \
    chmod 755 /home/user/backup && \
    chmod 755 /home/user/backup/logs && \
    chmod 755 /home/user/backup/verification

# Pre-populated rsync verification log
RUN cat > /home/user/backup/logs/rsync_2023-09-01.log <<'EOF'
2023/09/01 03:15:12 [12345] sent 123456 bytes  received 78910 bytes  total size 987654321
2023/09/01 03:15:12 [12345] verify /data/projects/app1/bin/run.sh OK
2023/09/01 03:15:12 [12345] verify /data/projects/app1/config/settings.yml FAILED checksum
2023/09/01 03:15:13 [12345] verify /data/images/logo.png OK
2023/09/01 03:15:13 [12345] verify /data/db/dump.sql FAILED size
2023/09/01 03:15:13 [12345] verify /data/docs/readme.md OK
2023/09/01 03:15:13 [12345] verify /data/secrets/keys.txt FAILED checksum
EOF

RUN chmod 644 /home/user/backup/logs/rsync_2023-09-01.log