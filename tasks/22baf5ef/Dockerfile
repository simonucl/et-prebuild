FROM ubuntu:22.04

# Author: release-manager-task-prep
# Description: Environment for the SQLite reporting task with pytest installed.

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 755 /home/user

RUN cat <<'SQL' | sqlite3 /home/user/release_info.db
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE deployments (
    id INTEGER PRIMARY KEY,
    project TEXT,
    environment TEXT,
    scheduled_date TEXT,
    status TEXT
);

INSERT INTO deployments (id, project, environment, scheduled_date, status) VALUES
    (1,'core-api','production','2024-01-10','completed'),
    (2,'core-api','staging','2024-01-10','completed'),
    (3,'analytics-service','production','2024-01-15','pending'),
    (4,'internal-tool','dev','2024-01-12','in_progress'),
    (5,'logging-service','production','2024-01-18','scheduled'),
    (6,'search','staging','2024-01-11','completed'),
    (7,'web-frontend','staging','2024-01-15','pending'),
    (8,'billing','production','2024-01-15','canceled');

COMMIT;
SQL

RUN chmod 666 /home/user/release_info.db

LABEL Author="release-manager-task-prep" \
      Description="Environment for the SQLite reporting task with pytest installed."