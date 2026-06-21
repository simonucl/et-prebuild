# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update package lists and install Python & pip
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest for the test runner
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create the required directory hierarchy
RUN mkdir -p /home/user/projects/cloud_migration/configs

# Populate the legacy INI file with the exact expected contents
RUN cat > /home/user/projects/cloud_migration/configs/legacy_service.ini << 'EOF'
[database]
host = legacy-db.internal
port = 5432
user = legacy_user
password = secret

[api]
endpoint = https://legacy-api.internal/v1
timeout = 30
EOF

# Ensure the non-root agent can write into the project tree
RUN chmod -R a+rwX /home/user

# Runtime environment setup
RUN chmod 755 /home/user
ENV PYTHONUNBUFFERED=1