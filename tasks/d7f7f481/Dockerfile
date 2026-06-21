FROM ubuntu:22.04

# Labels
LABEL Author="Tiny-Util Exercise Container"
LABEL Description="Container with initial state for YAML & TOML editing task"

# Post installation
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/project

# Create app.yaml
RUN cat << 'EOF' > /home/user/project/app.yaml
services:
  database:
    host: localhost
    port: 5432
EOF

# Create pyproject.toml
RUN cat << 'EOF' > /home/user/project/pyproject.toml
[tool.poetry]
name = "tiny-util"
version = "0.1.0"
description = "Small helper scripts"

[tool.poetry.dependencies]
python = "^3.9"
EOF

# Create README.md and set permissions
RUN echo "placeholder – irrelevant" > /home/user/project/README.md && \
    chmod -R a+rw /home/user/project && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Set working directory
WORKDIR /home/user

# Runscript equivalent
CMD echo "Container for Tiny-Util configuration editing exercise." && echo "Navigate to /home/user/project to begin."