FROM ubuntu:22.04

# Labels
LABEL Author="backup-task-preparer"
LABEL Description="Container image for SQLite backup task – provides initial company.db and Python/pytest tooling."

# System packages
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip sqlite3 openssl ca-certificates \
        tar gzip coreutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Python tooling
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# Create initial filesystem layout
RUN mkdir -p /home/user/data && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/data

# Build the initial SQLite database
RUN cat > /tmp/init.sql <<'EOSQL'
CREATE TABLE employees (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    department TEXT NOT NULL,
    salary     INTEGER NOT NULL
);
INSERT INTO employees (id, name, department, salary) VALUES
    (1, 'Alice',   'Engineering', 90000),
    (2, 'Bob',     'Sales',       75000),
    (3, 'Carol',   'HR',          68000),
    (4, 'Dave',    'Marketing',   72000),
    (5, 'Eve',     'Engineering', 95000);
EOSQL

RUN sqlite3 /home/user/data/company.db < /tmp/init.sql && \
    rm /tmp/init.sql && \
    chmod 0644 /home/user/data/company.db

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Set working directory
WORKDIR /home/user

# Default command
CMD ["/bin/bash"]

# Help information (as comments):
# This container supplies the initial state for the "cold backup" SQLite task.
# It includes:
#   • Ubuntu 22.04 base system
#   • sqlite3 CLI utility
#   • Python 3 with pytest pre-installed
#   • An example database at /home/user/data/company.db containing a single
#     table "employees" with exactly five rows.
#
# The /home/user/archive directory is intentionally NOT present.