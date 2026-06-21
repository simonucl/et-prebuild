FROM ubuntu:22.04

# Labels
LABEL Author="Backup-Verification Task"
LABEL Description="Environment providing initial SQLite database and tooling for the migration/validation exercise."

# Install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Create the canonical source database in a safe, read-only location
RUN mkdir -p /opt

RUN sqlite3 /opt/source_sales.db <<'SQL'
CREATE TABLE sales(
    id   INTEGER PRIMARY KEY,
    item TEXT,
    qty  INTEGER
);
INSERT INTO sales(item, qty) VALUES
    ('Widget',      10),
    ('Gadget',      20),
    ('Doodad',      15),
    ('Thingamajig', 5),
    ('Whatsit',     8);
SQL

# Make sure it is world-readable
RUN chmod 644 /opt/source_sales.db

# Clean up APT caches to keep the image small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create home directory and set up user environment
RUN mkdir -p /home/user && \
    chmod 755 /home/user

# Copy template database to user home directory
RUN cp /opt/source_sales.db /home/user/source_sales.db && \
    chmod 644 /home/user/source_sales.db

# Set environment variables
ENV HOME=/home/user

WORKDIR /home/user