# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------
# Install system dependencies and pytest
# ------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Create user home and directory structure
# ------------------------------------------------------------
RUN mkdir -p /home/user/db_configs && \
    chmod 755 /home/user

# ------------------------------------------------------------
# /home/user/db_configs/connection.ini
# ------------------------------------------------------------
RUN cat > /home/user/db_configs/connection.ini << 'EOF'
[development]
host=localhost
port=5432
user=dev
password=devpass
pool_size=5

[staging]
host=staging.db.internal
port=5432
user=staging
password=stagingpass
pool_size=10

[production]
host=prod.db.internal
port=5432
user=prod
password=prodpass
pool_size=20
EOF

# ------------------------------------------------------------
# /home/user/db_configs/queries.ini
# ------------------------------------------------------------
RUN cat > /home/user/db_configs/queries.ini << 'EOF'
[number_users]
query=SELECT COUNT(*) FROM users;
slow=no
priority=3

[big_join]
query=SELECT u.id, o.id FROM users u JOIN orders o ON u.id=o.user_id;
slow=yes
priority=2

[monthly_report]
query=SELECT * FROM reports WHERE month=CURRENT_DATE;
slow=yes
priority=5

[tmp_cleanup]
query=DELETE FROM temp WHERE created_at < NOW() - INTERVAL '1 day';
slow=no
priority=1

[yearly_stats]
query=SELECT * FROM stats_yearly;
slow=yes
priority=4
EOF

# ------------------------------------------------------------
# Set writable permissions for non-root agent
# ------------------------------------------------------------
RUN chmod 777 /home/user/db_configs && \
    chmod 666 /home/user/db_configs/*.ini

# ------------------------------------------------------------
# Metadata
# ------------------------------------------------------------
LABEL Author="task-prep" \
      Description="Environment for INI manipulation & report generation task."

# ------------------------------------------------------------
# Help
# ------------------------------------------------------------
# This image provides the initial state for the database-INI task.
# It contains:
#   - /home/user/db_configs/connection.ini
#   - /home/user/db_configs/queries.ini
# Pytest is pre-installed for the automated grader.
#
# The /home/user/reports/ directory is intentionally absent so
# that the agent’s script can create it during execution.