FROM ubuntu:22.04

# Author=ChatGPT
# Purpose=Initial state for audit-permissions task (pytest pre-checks ready)
# Container providing the starting environment for the “file-system permission audit” task.
# Includes:
#   • /home/user/audit/source_permissions.csv with the exact required content.
#   • pytest installed for the grading engine.
# Students are expected to create /home/user/audit/perm_overview.log.

RUN set -e && apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/audit && \
    chmod 755 /home/user && \
    chmod 777 /home/user/audit

RUN cat >/home/user/audit/source_permissions.csv <<'EOF'
path,user,group,perms
/etc/passwd,root,root,644
/etc/shadow,root,root,640
/var/log/syslog,syslog,adm,640
/home/user/.bashrc,user,user,600
/usr/bin/sudo,root,root,4755
/tmp/shared.txt,guest,guest,666
/var/www/html/index.html,www-data,www-data,644
EOF

RUN chmod 644 /home/user/audit/source_permissions.csv