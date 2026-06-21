FROM ubuntu:22.04

# Author backup-initializer
# Description "Environment prepared for monthly archive cycle exercise."

# This container image provides the pristine starting state for the
# "monthly archive cycle" exercise.  It includes the initial backup
# configuration files and has pytest installed for automated grading.
# Students should run the exercise commands after starting the container
# (no root privileges needed).

RUN set -e && \
    echo "Updating package index and installing Python tooling..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        build-essential && \
    echo "Installing pytest..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating initial directory tree and configuration files..." && \
    mkdir -p /home/user/backups/conf

# /home/user/backups/conf/backup.yaml  (initial, unedited content)
RUN cat > /home/user/backups/conf/backup.yaml <<'EOF'
schedule: "03:00"
directories:
  - /var/www
  - /home/projects
compression: "lz4"
retention_days: 30
EOF

# /home/user/backups/conf/storage.toml  (initial, unedited content)
RUN cat > /home/user/backups/conf/storage.toml <<'EOF'
[storage]
type = "s3"
bucket = "company-backups"
region = "us-east-1"

[credentials]
access_key = "REPLACE_ME"
secret_key = "REPLACE_ME"
EOF

RUN echo "Setting liberal permissions so the non-privileged runtime user can modify the files..." && \
    chmod 0775 /home/user /home/user/backups /home/user/backups/conf && \
    chmod 0666 /home/user/backups/conf/backup.yaml && \
    chmod 0666 /home/user/backups/conf/storage.toml && \
    echo "Cleaning up apt cache to minimize image size..." && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/user