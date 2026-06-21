FROM ubuntu:22.04

# Basic tooling
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata && \
    pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/projects/confmon/logs && \
    mkdir -p /home/user/projects/confmon/reports

# Set permissions
RUN chmod 0755 /home/user && \
    chmod 0755 /home/user/projects && \
    chmod 0755 /home/user/projects/confmon && \
    chmod 0755 /home/user/projects/confmon/logs && \
    chmod 0777 /home/user/projects/confmon/reports

# Seed the audit log
RUN cat > /home/user/projects/confmon/logs/config_changes.log <<'EOF'
2022-11-01 09:15:32 | jdoe | MODIFY | /etc/nginx/nginx.conf | SUCCESS
2022-11-01 10:45:03 | bgates | MODIFY | /etc/ssh/sshd_config | SUCCESS
2022-11-02 14:11:27 | jdoe | DELETE | /etc/apache2/sites-enabled/000-default.conf | SUCCESS
2022-10-31 12:00:00 | jdoe | MODIFY | /etc/passwd | FAILED
2022-11-15 16:42:05 | root | CREATE | /etc/sysctl.conf | SUCCESS
2022-11-20 08:22:18 | jdoe | MODIFY | /etc/nginx/nginx.conf | SUCCESS
2022-11-20 08:23:18 | jdoe | MODIFY | /etc/nginx/mime.types | SUCCESS
2022-11-30 23:59:59 | jdoe | DELETE | /etc/cron.d/backup | SUCCESS
2022-12-01 00:00:00 | jdoe | MODIFY | /etc/hosts | SUCCESS
2022-11-22 11:11:11 | alice | DELETE | /etc/ssh/ssh_config | FAILED
EOF

# Set log permissions
RUN chmod 0644 /home/user/projects/confmon/logs/config_changes.log

# Environment variables
ENV PYTHONIOENCODING=UTF-8

# Labels
LABEL Author="ExampleBuilder"
LABEL Description="Container for configuration monitoring task – seeded with baseline data and pytest installed."