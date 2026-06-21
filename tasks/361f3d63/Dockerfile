# Derived from Apptainer localimage bootstrap
FROM ubuntu:22.04

# Help text
# Converted from Apptainer definition file

RUN set -e && \
    echo "Updating APT and installing required packages..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        rsync \
        ca-certificates && \
    echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating initial directory structure and seed files for the rsync exercise..." && \
    mkdir -p /home/user/source_configs && \
    chmod 0777 /home/user/source_configs && \
    mkdir -p /home/user/remote_server/configs && \
    chmod 0777 /home/user/remote_server && \
    chmod 0777 /home/user/remote_server/configs && \
    chmod 0777 /home/user && \
    echo "Cleaning up apt caches..." && \
    rm -rf /var/lib/apt/lists/*

RUN cat <<'EOF' > /home/user/source_configs/app.conf
APP_ENV=production
MAX_CLIENTS=200
EOF

RUN cat <<'EOF' > /home/user/source_configs/db.conf
DB_HOST=postgres.internal
DB_PORT=5432
EOF

RUN cat <<'EOF' > /home/user/remote_server/configs/old.conf
legacy=true
EOF

RUN chmod -R 0666 /home/user/source_configs/*.conf && \
    chmod 0666 /home/user/remote_server/configs/old.conf

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH