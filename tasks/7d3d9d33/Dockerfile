# Author="Container build automation"
# Description="Environment for failed-login audit task with pre-populated SQLite database and pytest installed."
# This container image provides the starting state for the “failed-login audit”
# exercise. It includes:
# - A pre-populated SQLite DB at /home/user/audit/auth.db
# - Writable reports and logs directories
# - Python 3 and pytest for automated test execution

FROM ubuntu:22.04

RUN set -e \
    && apt-get update -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates \
    && pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/audit/reports \
    && mkdir -p /home/user/audit/logs

RUN cat <<'SQL' > /tmp/init.sql
PRAGMA journal_mode=OFF;
PRAGMA synchronous=OFF;

CREATE TABLE logins (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    success INTEGER NOT NULL,
    ts TEXT NOT NULL
);

INSERT INTO logins (id, username, success, ts) VALUES
    (1, 'alice', 1, '2023-05-01 10:00'),
    (2, 'bob',   0, '2023-05-01 10:05'),
    (3, 'alice', 0, '2023-05-01 10:06'),
    (4, 'carol', 0, '2023-05-01 10:07'),
    (5, 'bob',   0, '2023-05-01 10:08'),
    (6, 'alice', 0, '2023-05-01 10:09'),
    (7, 'dave',  1, '2023-05-01 10:10'),
    (8, 'carol', 1, '2023-05-01 10:11');
SQL

RUN sqlite3 /home/user/audit/auth.db < /tmp/init.sql \
    && rm /tmp/init.sql

RUN chmod 0777 /home/user/audit \
    && chmod 0777 /home/user/audit/reports \
    && chmod 0777 /home/user/audit/logs \
    && chmod 0666 /home/user/audit/auth.db \
    && chmod 755 /home/user

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH