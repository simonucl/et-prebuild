# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update APT and install Python + pip
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create required directory structure
RUN mkdir -p /home/user/system_configs && \
    chmod 755 /home/user && \
    chmod 755 /home/user/system_configs

# webapp.ini
RUN cat > /home/user/system_configs/webapp.ini <<'EOF'
[server]
port = 8080
enable_debug = true

[security]
secret_key = abc123
allowed_hosts = localhost,example.com
EOF

# db.ini
RUN cat > /home/user/system_configs/db.ini <<'EOF'
[database]
port = 1234
username = appuser
password = S3cur3Pass!

[options]
debug_mode = false
EOF

# cache.ini
RUN cat > /home/user/system_configs/cache.ini <<'EOF'
[cache]
port = 6379
enable_debug = false

[auth]
secret_key = veryverysecuresecret
EOF

# Set permissions on INI files
RUN chmod 644 /home/user/system_configs/*.ini

# Ensure the incident_logs directory does NOT exist initially
RUN rm -rf /home/user/incident_logs

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH