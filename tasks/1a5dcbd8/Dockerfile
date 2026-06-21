FROM ubuntu:22.04

# Help and labels
LABEL Author="filtered-copy-task-container"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/logs

RUN cat >/home/user/logs/config_changes.log <<'EOF'
[2023-05-01 09:15:23] CHANGED: /etc/nginx/nginx.conf
[2023-05-01 09:15:23] BACKUP: /etc/nginx/nginx.conf.bak
[2023-05-01 09:18:47] CHANGED: /etc/ssh/sshd_config
[2023-05-01 09:20:02] SKIPPED: /etc/hosts
[2023-05-01 09:21:10] CHANGED: /etc/php/php.ini
[2023-05-01 09:25:30] DRYRUN: /etc/fstab
[2023-05-01 09:27:54] CHANGED: /etc/systemd/system.conf
EOF

RUN chmod 0755 /home/user && \
    chmod 0755 /home/user/logs && \
    chmod 0644 /home/user/logs/config_changes.log