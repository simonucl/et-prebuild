FROM ubuntu:22.04

# Labels
LABEL Author="backup-ops-challenge"
LABEL Description="Container with initial state for the restore-preview task."

RUN set -e && \
    # Update APT and install Python & pip
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    # Ensure /home/user exists and is writable for the unprivileged agent
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    # Create /home/user/backups directory with correct permissions
    mkdir -p /home/user/backups && \
    chmod 0755 /home/user/backups

# Create the catalogue file with exact required contents
RUN cat >/home/user/backups/backup_filelist.txt <<'EOF'
/etc/nginx/nginx.conf
/etc/ssh/sshd_config
/var/www/html/index.html
/etc/mysql/my.cnf
/home/user/.bashrc
/etc/supervisor/supervisord.conf
/var/log/syslog
/etc/httpd/conf/httpd.conf
EOF

RUN chmod 0644 /home/user/backups/backup_filelist.txt && \
    # Clean up APT caches to keep image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/user

CMD ["bash", "-c", "chmod 755 /home/user && echo 'Container for backup restore-preview task. Launch an interactive shell.' && exec bash"]