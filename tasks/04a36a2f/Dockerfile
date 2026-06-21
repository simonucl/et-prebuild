FROM ubuntu:22.04

# Helpful defaults from %environment
ENV PYTHONUNBUFFERED=1

# Labels from %labels
LABEL Author="Your Name"
LABEL Description="Environment for the API log backup exercise with pre-seeded log files and pytest installed."

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/api_test/logs && \
    printf '{"request":"ping"}'   > /home/user/api_test/logs/request_20240601.json && \
    printf '{"response":"pong"}'  > /home/user/api_test/logs/response_20240601.json && \
    printf '{"error":null}'       > /home/user/api_test/logs/error_20240601.json && \
    chmod 644 /home/user/api_test/logs/*.json && \
    mkdir -p /home/user/api_test/backups && \
    chmod 755 /home/user/api_test/backups && \
    rm -f /home/user/api_test/backups/logs_backup_20240601.tar.gz && \
    rm -f /home/user/api_test/backups/latest_backup_manifest.txt