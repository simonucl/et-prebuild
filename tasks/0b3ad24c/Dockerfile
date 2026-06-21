FROM ubuntu:22.04

# Author: SRE Exercise Generator
# Version: v1.0
# This container image provides the starting environment for the
# “SQLite Uptime Monitoring” exercise. It already contains:
#   - /home/user/monitoring/uptime.db – pre-populated SQLite database
#   - sqlite3 CLI
#   - Python 3, pip, and pytest
# Students should extend the database and generate the required report.

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/monitoring && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/monitoring

RUN cat >/tmp/init.sql <<'EOF'
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS services (
    service_id   INTEGER PRIMARY KEY,
    service_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS service_checks (
    id           INTEGER PRIMARY KEY,
    service_name TEXT NOT NULL,
    status       TEXT CHECK(status IN ('up','down')) NOT NULL,
    timestamp    TEXT NOT NULL
);

DELETE FROM services;
DELETE FROM service_checks;

INSERT INTO services (service_id, service_name) VALUES
    (10, 'frontend'),
    (11, 'backend');

INSERT INTO service_checks (id, service_name, status, timestamp) VALUES
    (1, 'frontend', 'up',   '2023-05-15T09:30:00Z'),
    (2, 'backend',  'up',   '2023-05-15T09:30:00Z'),
    (3, 'frontend', 'up',   '2023-05-15T09:45:00Z'),
    (4, 'backend',  'up',   '2023-05-15T09:45:00Z'),
    (5, 'frontend', 'down', '2023-05-15T09:55:00Z'),
    (6, 'backend',  'up',   '2023-05-15T09:55:00Z');

COMMIT;
EOF

RUN sqlite3 /home/user/monitoring/uptime.db < /tmp/init.sql && \
    chmod 0644 /home/user/monitoring/uptime.db && \
    rm -f /tmp/init.sql && \
    chmod 755 /home/user

CMD echo "Container for SRE SQLite uptime exercise." && \
    echo "Open a shell with 'docker run -it' or exec into it to run your solution."