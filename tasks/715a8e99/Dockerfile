# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: Container Provisioner
# Description: Provides the initial state for the SQLite migration task, including the pre-populated source database and pytest installation.

LABEL Author="Container Provisioner" \
      Description="Provides the initial state for the SQLite migration task, including the pre-populated source database and pytest installation."

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the forthcoming test harness
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create the /home/user directory if it doesn't yet exist
RUN mkdir -p /home/user

# Build the source SQLite database with the required table and rows
RUN python3 - <<'PYTHON'
import os, sqlite3

db_path = "/home/user/source_data.db"
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# (Re)create the database to ensure a clean, deterministic state
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
conn.execute("CREATE TABLE dataset (id INTEGER PRIMARY KEY, value TEXT)")
conn.executemany(
    "INSERT INTO dataset (id, value) VALUES (?, ?)",
    [(1, "alpha"), (2, "beta"), (3, "gamma")]
)
conn.commit()
conn.close()

# Make the database world-readable/writable so a non-root agent can access it
os.chmod(db_path, 0o666)
PYTHON

# Ensure ownership of /home/user is set to the build-time user
RUN chown -R $(id -u):$(id -g) /home/user || true

# Set permissions on /home/user
RUN chmod 755 /home/user

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1