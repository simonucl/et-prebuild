# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# -----------------------------------------------------------------
# Install required packages
# -----------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test harness
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# -----------------------------------------------------------------
# Prepare the initial filesystem state expected by the test suite
# -----------------------------------------------------------------

# Ensure /home/user exists with correct permissions
RUN mkdir -p /home/user && \
    chmod 755 /home/user

# Create the helpdesk directory
RUN mkdir -p /home/user/helpdesk && \
    chmod 755 /home/user/helpdesk

# Build the SQLite database with the required schema and data
RUN cat <<'SQL' | sqlite3 /home/user/helpdesk/helpdesk.db
CREATE TABLE tickets (
    id      INTEGER PRIMARY KEY,
    title   TEXT,
    status  TEXT
);
INSERT INTO tickets VALUES
    (1,'Cannot connect to VPN','open'),
    (2,'Email not syncing','open'),
    (3,'Forgot password','resolved'),
    (4,'Printer jam','in_progress');
SQL

# Set database file permissions
RUN chmod 644 /home/user/helpdesk/helpdesk.db

# -----------------------------------------------------------------
# %environment
# No special environment variables are required
# -----------------------------------------------------------------