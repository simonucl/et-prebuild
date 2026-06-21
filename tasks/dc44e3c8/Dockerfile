FROM ubuntu:22.04

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Update package lists and install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        sqlite3 \
        python3 \
        python3-pip

# Install the latest pytest via pip
RUN pip3 install --no-cache-dir --upgrade pytest

# Prepare initial filesystem state for the migration exercise
RUN mkdir -p /home/user

# Create the legacy SQLite database with the prescribed schema & data
RUN sqlite3 /home/user/observability.db <<'SQL'
PRAGMA journal_mode=WAL;
CREATE TABLE metrics (id INTEGER PRIMARY KEY, name TEXT, value REAL);
INSERT INTO metrics VALUES
  (1,'cpu_usage',0.75),
  (2,'mem_usage',0.60),
  (3,'disk_io',123.45);
SQL

# Ensure permissive permissions so the non-root agent can read/write
RUN chmod -R a+rwX /home/user

# Labels
LABEL Author="Apptainer Task Preparer"
LABEL Description="Container providing initial state for SQLite migration task with pytest installed."