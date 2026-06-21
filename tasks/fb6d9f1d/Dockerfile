FROM ubuntu:22.04

# Update package index and install required tools
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        diffutils \
        patch \
        coreutils

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/backup_snapshot_2023-01-15 && \
    mkdir -p /home/user/service_config && \
    mkdir -p /home/user/restore_work

# Populate snapshot files (pristine references)
RUN cat > /home/user/backup_snapshot_2023-01-15/httpd.conf <<'EOF'
ServerRoot "/etc/httpd"
Listen 80
LoadModule dir_module modules/mod_dir.so
Include conf/extra/httpd-vhosts.conf
EOF

RUN cat > /home/user/backup_snapshot_2023-01-15/app.env <<'EOF'
DB_HOST=prod-db.internal
DB_PORT=5432
DB_USER=app
DB_PASS=secret
APP_ENV=production
EOF

# Populate service config files (contain drift)
RUN cat > /home/user/service_config/httpd.conf <<'EOF'
ServerRoot "/etc/httpd"
Listen 8080
LoadModule dir_module modules/mod_dir.so
EOF

RUN cat > /home/user/service_config/app.env <<'EOF'
DB_HOST=prod-db.internal
DB_PORT=5432
DB_USER=app
APP_ENV=production
EOF

# Permissions
# Snapshot: read-only for users (agent only needs to read)
RUN chmod 0644 /home/user/backup_snapshot_2023-01-15/httpd.conf && \
    chmod 0644 /home/user/backup_snapshot_2023-01-15/app.env

# Service config: writable so the unprivileged agent can patch them
RUN chmod 0666 /home/user/service_config/httpd.conf && \
    chmod 0666 /home/user/service_config/app.env

# Directory permissions
RUN chmod 0755 /home/user/backup_snapshot_2023-01-15 && \
    chmod 0777 /home/user/service_config && \
    chmod 0777 /home/user/restore_work && \
    chmod 0755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1

WORKDIR /home/user