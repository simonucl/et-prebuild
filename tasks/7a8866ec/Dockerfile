# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install required system packages
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-venv \
        sqlite3 && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Install pytest (used by the grading harness)
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare filesystem structure and SQLite database
# ------------------------------------------------------------------
RUN mkdir -p /home/user/projects/profile

RUN sqlite3 /home/user/projects/profile/data.db <<'SQL'
CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY,
    component TEXT,
    cpu_usage REAL
);
DELETE FROM metrics;
INSERT INTO metrics (id, component, cpu_usage) VALUES
    (1, 'auth', 55.2),
    (2, 'api', 70.8),
    (3, 'db', 65.0),
    (4, 'ui', 40.0);
SQL

# ------------------------------------------------------------------
# Adjust permissions so the unprivileged runtime user can write under /home/user
# ------------------------------------------------------------------
RUN chmod -R 0777 /home/user

# ------------------------------------------------------------------
# Default command (replacement for %runscript)
# ------------------------------------------------------------------
CMD ["bash"]