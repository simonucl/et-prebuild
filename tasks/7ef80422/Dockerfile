FROM ubuntu:22.04

# Help / metadata (from %labels)
LABEL Author="backup-task-builder"
LABEL Description="Apptainer image for the backup verification exercise with pytest pre-installed."

ENV DEBIAN_FRONTEND=noninteractive

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tar \
        gzip && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/backup_src

RUN cat > /home/user/backup_src/file1.txt <<'EOF'
Report id: FQ1-2024
Total revenue: $1,000,000
EOF

RUN cat > /home/user/backup_src/file2.txt <<'EOF'
HR internal directory v2.3
Last updated: 2024-05-12
EOF

RUN chmod 777 /home/user/backup_src && \
    chmod 666 /home/user/backup_src/file1.txt /home/user/backup_src/file2.txt && \
    chmod 755 /home/user