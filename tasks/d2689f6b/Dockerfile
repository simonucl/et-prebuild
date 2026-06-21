FROM ubuntu:22.04

# Install required tools
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user/legacy && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create the legacy database with the required schema and rows
RUN sqlite3 /home/user/legacy/old_db.sqlite <<'SQL'
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    department TEXT
);
INSERT INTO employees (id, first_name, last_name, department) VALUES
    (1,'Ava','Moore','Engineering'),
    (2,'Liam','Johnson','Finance'),
    (3,'Emma','Davis','Marketing'),
    (4,'Noah','Wilson','HR'),
    (5,'Mia','Brown','Sales');
SQL

# Ensure the /home/user directory tree is writable by any non-root user
RUN chmod -R 0777 /home/user

# Set environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8