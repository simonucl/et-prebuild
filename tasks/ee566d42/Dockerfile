FROM ubuntu:22.04

# Basic OS tools + pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state for the grading tests
RUN mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/data/logs && \
    mkdir -p /home/user/data/backup && \
    mkdir -p /home/user/data/public && \
    mkdir -p /home/user/data/private

# Files with exact sizes and permissions
RUN truncate -s 62914560 /home/user/data/logs/app.log && chmod 0666 /home/user/data/logs/app.log
RUN truncate -s 125829120 /home/user/data/backup/db.dump && chmod 0600 /home/user/data/backup/db.dump
RUN truncate -s 73400320 /home/user/data/public/video.mp4 && chmod 0666 /home/user/data/public/video.mp4
RUN truncate -s 1024 /home/user/data/public/readme.txt && chmod 0666 /home/user/data/public/readme.txt
RUN truncate -s 57671680 /home/user/data/private/secret.txt && chmod 0600 /home/user/data/private/secret.txt

# Environment adjustments from %environment
RUN chmod 755 /home/user
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin

# Labels
LABEL Author="ExampleAuthor"
LABEL Description="Initial state for security-meets-capacity spot-check task"