# Container image for the "log-summary" exercise.
# Provides the initial log file at /home/user/logs/app.log and
# includes pytest for automated testing.

FROM ubuntu:22.04

LABEL Author="devops-task-prep"

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/logs

RUN cat <<'EOF' >/home/user/logs/app.log
2023-08-14 10:15:23 INFO User login success
2023-08-14 10:17:01 ERROR Failed to connect to DB
2023-08-15 07:02:11 WARN Disk usage high
2023-08-15 08:33:48 ERROR Timeout while reading configuration
2023-08-15 09:01:10 ERROR Invalid user input
2023-08-15 14:22:59 ERROR Connection reset by peer
2023-08-16 12:45:00 INFO Routine maintenance started
EOF

RUN chmod 755 /home/user/logs && \
    chmod 644 /home/user/logs/app.log