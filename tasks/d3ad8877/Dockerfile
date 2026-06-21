FROM ubuntu:22.04

# Labels
LABEL Maintainer="Configuration Manager Task – Apptainer setup"

# Update package list and install Python + pip
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem expected by the tests
RUN mkdir -p /home/user/configs/nginx/sites-available && \
    mkdir -p /home/user/configs/app/db && \
    mkdir -p /home/user/configs/obsolete

# nginx/nginx.conf
RUN printf 'user  www-data;\nworker_processes  auto;\npid /run/nginx.pid;\n' \
    > /home/user/configs/nginx/nginx.conf

# nginx/sites-available/default.conf
RUN printf 'server {\n    listen 80 default_server;\n    server_name _;\n    root /var/www/html;\n}\n' \
    > /home/user/configs/nginx/sites-available/default.conf

# app/app.conf
RUN printf '[app]\nname = SampleApp\nversion = 1.2.3\n' \
    > /home/user/configs/app/app.conf

# app/db/database.conf
RUN printf '[database]\nhost = localhost\nport = 5432\n' \
    > /home/user/configs/app/db/database.conf

# obsolete/old.conf
RUN printf 'deprecated=true\n' \
    > /home/user/configs/obsolete/old.conf

# Set modification timestamps
#   • recent files  : now - 2 days
#   • obsolete file : now - 90 days
RUN touch -d '2 days ago' /home/user/configs/nginx/nginx.conf && \
    touch -d '2 days ago' /home/user/configs/nginx/sites-available/default.conf && \
    touch -d '2 days ago' /home/user/configs/app/app.conf && \
    touch -d '2 days ago' /home/user/configs/app/db/database.conf && \
    touch -d '90 days ago' /home/user/configs/obsolete/old.conf

# Ensure the backup target does NOT exist initially
RUN rm -rf /home/user/configs_recent_backup

# Make /home/user writable for the unprivileged runtime user
RUN chmod -R a+rwX /home/user

# Environment variables
ENV PYTHONUNBUFFERED=1