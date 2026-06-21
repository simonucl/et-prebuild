# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Prepare initial on-disk state expected by the autograder
# ------------------------------------------------------------------
RUN mkdir -p /home/user/db_backup

# Create config.yaml with the INITIAL content
RUN cat > /home/user/db_backup/config.yaml <<'EOF'
database:
  host: "localhost"
  port: 5432
  name: "maindb"
backup:
  enabled: false
  schedule: "not_set"
  compression: "none"
EOF

# Create retention.toml with the INITIAL content
RUN cat > /home/user/db_backup/retention.toml <<'EOF'
[retention]
max_backups = 0
keep_days   = 0
cold_storage = true
EOF

# Do NOT create changes.log – it must not exist at start

# Make sure the regular (non-root) user can read/write these files
RUN chmod 777 /home/user && \
    chmod 777 /home/user/db_backup && \
    chmod 666 /home/user/db_backup/config.yaml /home/user/db_backup/retention.toml

# Environment setup
RUN chmod 755 /home/user
ENV PYTHONUNBUFFERED=1

# %help
# Container with Python, pytest, and initialized backup configuration files for autograding.