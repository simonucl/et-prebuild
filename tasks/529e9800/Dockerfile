FROM ubuntu:22.04

# Help / labels from %labels
LABEL Author="Apptainer Setup Script"
LABEL Description="Environment for the configuration-manager synchronisation task with pytest pre-installed."

# ------------------------------------------------------------------
# 1. System packages
# ------------------------------------------------------------------
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        rsync \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# 2. PyPI packages
# ------------------------------------------------------------------
RUN pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# 3. Prepare initial directory tree and files
# ------------------------------------------------------------------
RUN mkdir -p /home/user/config_manager/workdir

RUN cat << 'EOF' > /home/user/config_manager/workdir/app.conf
version=1.0
EOF

RUN cat << 'EOF' > /home/user/config_manager/workdir/db.conf
host=localhost
port=5432
EOF

RUN mkdir -p /home/user/remote_configs

RUN cat << 'EOF' > /home/user/remote_configs/app.conf
version=1.1
EOF

RUN cat << 'EOF' > /home/user/remote_configs/db.conf
host=localhost
port=5432
EOF

RUN cat << 'EOF' > /home/user/remote_configs/cache.conf
enabled=true
EOF

# ------------------------------------------------------------------
# 4. Permissions
# ------------------------------------------------------------------
RUN chmod -R a+rwX /home/user

# ------------------------------------------------------------------
# Environment variables from %environment
# ------------------------------------------------------------------
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN chmod 755 /home/user