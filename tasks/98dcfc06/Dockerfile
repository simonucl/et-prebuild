FROM ubuntu:22.04

# Labels from %labels
LABEL Author="Auto-generated for backup-restore validation task"
LABEL Description="Environment with initial CSV logs and pytest pre-installed."

# Environment variables from %environment
ENV PATH=/usr/bin:$PATH

# System packages and Python tooling
RUN set -eu && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directory structure
RUN mkdir -p /home/user/restore_tests/raw_logs

# Create log_day1.csv
RUN cat >/home/user/restore_tests/raw_logs/log_day1.csv <<'EOF'
2023-09-01T02:13:22Z,/etc/nginx/nginx.conf,RESTORED
2023-09-01T02:14:01Z,/var/www/html/index.html,RESTORED
2023-09-01T02:14:45Z,/etc/nginx/nginx.conf,RESTORED
2023-09-01T02:15:10Z,/var/www/html/index.html,FAILURE
2023-09-01T02:15:55Z,/home/user/.bashrc,RESTORED
2023-09-01T02:16:27Z,/etc/nginx/nginx.conf,RESTORED
2023-09-01T02:17:08Z,/var/www/html/main.css,RESTORED
EOF

# Create log_day2.csv
RUN cat >/home/user/restore_tests/raw_logs/log_day2.csv <<'EOF'
2023-09-02T11:05:00Z,/etc/nginx/nginx.conf,RESTORED
2023-09-02T11:06:14Z,/var/www/html/index.html,RESTORED
2023-09-02T11:06:52Z,/home/user/.bashrc,RESTORED
2023-09-02T11:07:33Z,/var/www/html/main.css,RESTORED
2023-09-02T11:08:17Z,/etc/nginx/nginx.conf,RESTORED
2023-09-02T11:08:59Z,/home/user/.bashrc,FAILURE
2023-09-02T11:09:41Z,/var/www/html/index.html,RESTORED
EOF

# Permissions
RUN chmod 755 /home/user && \
    chmod -R 755 /home/user/restore_tests && \
    chmod 644 /home/user/restore_tests/raw_logs/log_day1.csv && \
    chmod 644 /home/user/restore_tests/raw_logs/log_day2.csv