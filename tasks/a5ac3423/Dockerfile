FROM ubuntu:22.04

# Basic tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare filesystem expected by the tests
RUN mkdir -p /home/user/data/projects/projA/subdir && \
    mkdir -p /home/user/data/projects/projB && \
    mkdir -p /home/user/archives && \
    chmod 777 /home/user/archives

RUN printf "2023-01-15 10:00:00 INFO Application started\n" > /home/user/data/projects/projA/app.log && \
    printf "DEBUG: variable x=42\nDEBUG: variable y=84\n" > /home/user/data/projects/projA/debug.log && \
    printf "Legacy log file\nLine2\n" > /home/user/data/projects/projA/subdir/legacy.log && \
    printf "2023-02-20 12:00:00 ERROR Unexpected shutdown\n" > /home/user/data/projects/projB/server.log && \
    printf "Some notes that should stay after cleanup.\n" > /home/user/data/projects/projA/notes.txt && \
    printf "# Project B readme\nThis file must remain.\n" > /home/user/data/projects/projB/readme.md

# Environment settings
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin

LABEL Author="Backup-task container preparer"
LABEL Task="Initial state for *.log backup/cleanup exercise"