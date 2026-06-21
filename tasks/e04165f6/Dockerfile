FROM ubuntu:22.04

# Labels
LABEL Author="Backup-Exercise-Prep"
LABEL Description="Environment prepared for backup-testing exercise with pytest pre-installed."

# Environment variables
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV PYTHONIOENCODING=utf-8

# ----------------------------
# 1) System prerequisites
# ----------------------------
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        locales && \
    sed -i 's/^# *\(en_US.UTF-8\)/\1/' /etc/locale.gen && \
    locale-gen && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ----------------------------
# 2) Create initial directory tree and manifest CSV files
# ----------------------------
RUN mkdir -p /home/user/backup_testing/manifests

# Daily manifest
RUN cat > /home/user/backup_testing/manifests/daily_restore_2023-01-15.csv <<'EOF'
ID,FILE_PATH,ORIGINAL_SIZE,RESTORED_SIZE,STATUS,CRC32
1,/data/db1.sql,1048576,1048576,OK,3A5F1D2C
2,/data/db2.sql,2048000,2048000,OK,B2C4E6F3
3,/data/db3.sql,1048576,1048572,WARNING,D3A7C9E4
EOF

# Weekly manifest
RUN cat > /home/user/backup_testing/manifests/weekly_restore_2023-01-15.csv <<'EOF'
ID,FILE_PATH,ORIGINAL_SIZE,RESTORED_SIZE,STATUS,CRC32
1,/backup/www.tar.gz,4096000,4096000,OK,9C1D2E3F
2,/backup/mail.tar.gz,2097152,2097152,OK,AA11BB22
3,/backup/home.tar.gz,3145728,3145720,WARNING,CC33DD44
4,/backup/configs.tar.gz,512000,512000,OK,EE44FF55
EOF

# ----------------------------
# 3) Permissions
# ----------------------------
RUN chmod 0777 /home/user/backup_testing && \
    chmod -R a+rX /home/user/backup_testing/manifests && \
    chmod 755 /home/user

WORKDIR /home/user

CMD ["echo", "Container for the backup-testing exercise. Use an interactive shell to begin."]