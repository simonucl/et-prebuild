# syntax=docker/dockerfile:1
# Based on localimage ./ubuntu_22.04.sif -> approximated as ubuntu:22.04
FROM ubuntu:22.04

# Install system packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    sqlite3 \
    ca-certificates \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Prepare filesystem structure
RUN mkdir -p /home/user/legacy && mkdir -p /home/user/new && chmod -R 777 /home/user

# Create legacy SQLite database
RUN sqlite3 /home/user/legacy/legacy.db <<'SQL'
CREATE TABLE customers_old (
    id    INTEGER PRIMARY KEY,
    name  TEXT,
    email TEXT
);
INSERT INTO customers_old (id, name, email) VALUES
    (1,'Alice Smith','alice@example.com'),
    (2,'Bob Jones','bob@example.com'),
    (3,'Charlie Brown','charlie@example.com');
SQL

# Ensure DB is writable
RUN chmod 666 /home/user/legacy/legacy.db

# Permissions expected by environment block
RUN chmod 755 /home/user

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV LC_ALL=C

# Labels
LABEL Author="Container prep script"
LABEL Description="Initial environment for SQLite migration task with pytest installed."