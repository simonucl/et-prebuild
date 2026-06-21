FROM ubuntu:22.04

# Help / labels
LABEL Author="Container Prep Utility"
LABEL Description="Environment for SQLite counting task (includes pytest and test DB)"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip sqlite3 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 0777 /home/user

RUN mkdir -p /home/user/microservices && chmod 0755 /home/user/microservices

RUN SQLITE_DB=/home/user/microservices/logs.db && \
    mkdir -p /home/user/microservices && \
    sqlite3 "${SQLITE_DB}" <<'SQL_EOF'
PRAGMA journal_mode = OFF;
CREATE TABLE services (
    id     INTEGER PRIMARY KEY,
    name   TEXT    NOT NULL,
    status TEXT    NOT NULL
);

INSERT INTO services (id, name, status) VALUES
    (1, 'auth-api',     'running'),
    (2, 'payments-api', 'stopped'),
    (3, 'user-api',     'running'),
    (4, 'metrics',      'running'),
    (5, 'gateway',      'stopped');
SQL_EOF

RUN chmod 0644 /home/user/microservices/logs.db

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin