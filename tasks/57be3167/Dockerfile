# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Updating package list & installing Python tooling...
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the runtime environment
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

############################################################################
# Create initial filesystem state for the “site-admin” task
############################################################################
RUN set -e && \
    BASE_DIR="/home/user/site-admin" && \
    CONF_DIR="${BASE_DIR}/conf" && \
    LOGS_DIR="${BASE_DIR}/logs" && \
    mkdir -p "${CONF_DIR}" "${LOGS_DIR}"

# Create accounts.db with the required initial records (single trailing \n)
RUN cat > "/home/user/site-admin/conf/accounts.db" <<'EOF'
alice:1000:admin:active
bob:1001:editor:inactive
carol:1002:viewer:active
EOF

# Create account_changes.log with the required initial audit line
RUN cat > "/home/user/site-admin/logs/account_changes.log" <<'EOF'
[2023-01-14 09:30:00] ADD carol 1002 viewer active
EOF

# Ensure the non-root user that will run the container can read/write
RUN chmod -R 0777 /home/user/site-admin && \
    chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# %help
# This container provides a Python environment with pytest installed and
# initializes a site-admin filesystem layout under /home/user/site-admin.