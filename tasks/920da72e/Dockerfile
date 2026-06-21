FROM ubuntu:22.04

LABEL Author="Storage-Cleanup-Setup"
LABEL Description="Initial filesystem state and tooling for disk_cleanup task"

ENV PATH="/home/user/bin:$PATH"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/data/incoming && \
    mkdir -p /home/user/archive && \
    mkdir -p /home/user/logs && \
    mkdir -p /home/user/bin && \
    chmod 755 /home/user && \
    chmod 755 /home/user/data && \
    chmod 755 /home/user/data/incoming && \
    chmod 755 /home/user/archive && \
    chmod 755 /home/user/logs && \
    chmod 755 /home/user/bin

RUN truncate -s 2048 /home/user/data/incoming/log1.txt && \
    truncate -s 5242880 /home/user/data/incoming/old_report.tar && \
    truncate -s 15728640 /home/user/data/incoming/video.mp4 && \
    chmod 644 /home/user/data/incoming/log1.txt && \
    chmod 644 /home/user/data/incoming/old_report.tar && \
    chmod 644 /home/user/data/incoming/video.mp4

RUN rm -f /home/user/bin/disk_cleanup.sh || true

# Container for disk_cleanup exercise. Nothing to run by default.