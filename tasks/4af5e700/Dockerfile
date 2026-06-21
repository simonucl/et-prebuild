FROM ubuntu:22.04

# Help / description
# Author: log-analysis-initializer
# Description: Container prepared for the log-analysis task. Provides initial logs, cron tooling, and pytest.

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONIOENCODING=utf-8

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        cron \
        python3-pip \
        python3-setuptools \
        ca-certificates \
        tzdata && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/logs

RUN cat > /home/user/logs/system_events.log <<'EOF'
[2023-04-01 10:00:00] INFO User login: alice
[2023-04-01 10:05:00] WARNING Disk space low on /dev/sda1
[2023-04-01 10:07:24] ERROR Failed to connect to database
[2023-04-01 10:15:42] INFO Scheduled backup started
[2023-04-01 10:45:13] INFO Scheduled backup completed
[2023-04-01 11:00:00] ERROR Failed to send email
[2023-04-01 11:30:23] WARNING High memory usage detected
[2023-04-01 11:45:23] INFO User logout: alice
[2023-04-01 12:00:00] INFO User login: bob
EOF

RUN chmod 755 /home/user/logs && \
    chmod 644 /home/user/logs/system_events.log && \
    chmod 755 /home/user

LABEL Author="log-analysis-initializer"
LABEL Description="Container prepared for the log-analysis task. Provides initial logs, cron tooling, and pytest."