FROM ubuntu:22.04

# Help / labels
LABEL Author="Apptainer Task Setup"
LABEL Description="Environment with legacy SQLite DB and pytest pre-installed."

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/legacy_app/data && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/legacy_app && \
    chmod 0755 /home/user/legacy_app/data

RUN sqlite3 /home/user/legacy_app/data/old_users.db <<'SQL'
PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;
CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username TEXT,
    email TEXT
);
INSERT INTO users (id, username, email) VALUES
    (1, 'alice', 'alice@example.com'),
    (2, 'bob', 'bob@example.com'),
    (3, 'carol', 'carol@example.com'),
    (4, 'dave', 'dave@example.com'),
    (5, 'eve', 'eve@example.com');
COMMIT;
SQL

RUN chmod 0644 /home/user/legacy_app/data/old_users.db

RUN apt-get clean && rm -rf /var/lib/apt/lists/*