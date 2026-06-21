# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python, pip, and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Create user and home directory
# ------------------------------------------------------------------
RUN set -e && \
    useradd -m -d /home/user -s /bin/bash user

# ------------------------------------------------------------------
# Prepare initial exercise data
# ------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user/migration

RUN cat > /home/user/migration/service_endpoints.log <<'EOF'
api-us.example.com
api-eu.example.com
api-us.example.com
api-us.example.com
auth.example.com
api-eu.example.com
cdn.example.com
auth.example.com
auth.example.com
cdn.example.com
cdn.example.com
cdn.example.com
EOF

# ------------------------------------------------------------------
# Permissions (default umask 022 → 0644 for files, 0755 for dirs)
# ------------------------------------------------------------------
RUN set -e && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/migration && \
    chmod 0644 /home/user/migration/service_endpoints.log && \
    chown -R user:user /home/user

# ------------------------------------------------------------------
# Environment variables
# ------------------------------------------------------------------
ENV LC_ALL=C \
    LANG=C

# Default command: exec passed commands (similar to Apptainer runscript)
CMD ["bash"]