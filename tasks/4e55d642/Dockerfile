FROM ubuntu:22.04

# Author: Task Builder
# Purpose: Starter image for the configuration-management exercise
# This container sets up the initial environment for the webserver
# configuration task. The directory /home/user/configs contains
# webserver.conf with predefined settings. Pytest is available for automated grading.

LABEL Author="Task Builder"
LABEL Purpose="Starter image for the configuration-management exercise"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/configs

RUN cat <<'EOF' > /home/user/configs/webserver.conf
# Web Server Configuration
ENABLE_LOGS=false
MAX_USERS=50
PORT=8080
TIMEZONE=UTC
EOF

RUN chmod 755 /home/user/configs && \
    chmod 644 /home/user/configs/webserver.conf