FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Ensure /home/user exists
RUN mkdir -p /home/user/project/config

# Create app.yaml
RUN cat <<'EOF' > /home/user/project/config/app.yaml
name: SampleApp
version: 1.2.3
settings:
  debug: false
  max_connections: 50
EOF

# Create database.toml
RUN cat <<'EOF' > /home/user/project/config/database.toml
[database]
host = "localhost"
port = 5432
user = "appuser"
password = "secret"
timeout = 30
EOF

# Set correct permissions
RUN chmod 644 /home/user/project/config/app.yaml /home/user/project/config/database.toml

# Apply chmod from %environment
RUN chmod 755 /home/user

# Environment variables
ENV PYTHONUNBUFFERED=1