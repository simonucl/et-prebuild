FROM ubuntu:22.04

# Help and metadata
LABEL Author="backup-task-container"
LABEL Description="Initial state for the backup & symlink exercise with pytest installed."

# Environment
ENV LANG=C.UTF-8

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create initial filesystem state
RUN set -e && \
    mkdir -p /home/user/data/projectA && \
    mkdir -p /home/user/data/projectB && \
    mkdir -p /home/user/data/projectC && \
    mkdir -p /home/user/backups && \
    printf "server-log-A-1\nserver-log-A-2\n" > /home/user/data/projectA/server.log && \
    printf "error-A-1\n" > /home/user/data/projectA/error.log && \
    printf "access-B-entry\n" > /home/user/data/projectB/access.log && \
    printf "debug-B-trace\n" > /home/user/data/projectB/debug.log && \
    printf "app-C-start\n" > /home/user/data/projectC/app.log && \
    printf "README A\n" > /home/user/data/projectA/readme.txt && \
    printf "setting: B\n" > /home/user/data/projectB/config.yml && \
    printf "Notes C\n" > /home/user/data/projectC/notes.md

# Permissions
RUN chmod -R a+rwX /home/user && chmod 755 /home/user