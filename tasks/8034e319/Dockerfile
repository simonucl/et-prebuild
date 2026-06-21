# Converted from Apptainer definition
FROM ubuntu:22.04

# Update base image and install Python + PyPI tooling
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/provisioning/config

# Create app.yml
RUN cat <<'EOF' > /home/user/provisioning/config/app.yml
service:
  name: webapp
  port: 8000
  debug: false
EOF

# Create db.toml
RUN cat <<'EOF' > /home/user/provisioning/config/db.toml
[connection]
user = "admin"
password = "secret"
host = "localhost"
port = 5432
max_connections = 100
EOF

# Permissions
RUN chmod -R 777 /home/user

# Environment variables (from %environment)
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Apply chmod from %environment (cannot be an ENV)
RUN chmod 755 /home/user