FROM ubuntu:22.04

# Labels
LABEL Author="example@example.com"

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip install --no-cache-dir pytest

# Create required directory structure
RUN mkdir -p /home/user/app/config && \
    mkdir -p /home/user/logs

# Populate configuration files with initial contents
RUN cat <<'EOF' >/home/user/app/config/service.yaml
# orders service configuration
maintenance_mode: false
port: 8080
EOF

RUN cat <<'EOF' >/home/user/app/config/service.toml
# orders service configuration
maintenance_mode = false
port = 8080
EOF

# Ensure non-root users can modify the files and directories
RUN chmod -R 777 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"