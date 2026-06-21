# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: configuration-task
# Description: Container for configuration summary task – includes pytest and initial log setup

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    if ! getent group 1000 >/dev/null 2>&1; then groupadd -g 1000 user; fi && \
    if ! id -u 1000 >/dev/null 2>&1; then useradd -m -u 1000 -g 1000 -s /bin/bash user; fi && \
    mkdir -p /home/user/config_logs && \
    chown user:user /home/user /home/user/config_logs && \
    chmod 0755 /home/user/config_logs

RUN cat <<'EOF' > /home/user/config_logs/changes.log
[2023-07-18 09:15:23] user=alice file=/etc/nginx/nginx.conf action=modified
[2023-07-18 10:41:02] user=bob file=/etc/ssh/sshd_config action=modified
[2023-07-19 08:20:17] user=alice file=/etc/nginx/sites-enabled/default action=created
[2023-07-19 11:05:44] user=carol file=/etc/cron.d/backup action=deleted
[2023-07-20 14:12:31] user=bob file=/etc/hosts action=modified
[2023-07-21 07:55:09] user=alice file=/etc/nginx/nginx.conf action=modified
[2023-07-21 12:00:00] user=carol file=/etc/passwd action=modified
[2023-07-22 09:30:45] user=alice file=/etc/nginx/sites-available/site1 action=created
EOF

RUN chown user:user /home/user/config_logs/changes.log && \
    chmod 0644 /home/user/config_logs/changes.log && \
    chmod 755 /home/user

ENV PYTHONIOENCODING=UTF-8