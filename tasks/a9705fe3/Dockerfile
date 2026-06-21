# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help:
# This container supplies the starting state for the i18n SQLite exercise.
# It contains:
#   * /home/user/projects/i18n/messages.db – pre-populated with two rows
#   * python3, sqlite3 CLI, and pytest – tools required by the assignment

LABEL Author="Container generated for i18n SQLite task"
LABEL Description="Provides initial environment with messages.db and pytest installed."

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        locales \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    sed -i 's/# *en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/projects/i18n

RUN sqlite3 /home/user/projects/i18n/messages.db <<'SQL'
PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;
CREATE TABLE translations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    language TEXT NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL
);
INSERT INTO translations (language, key, value) VALUES
    ('en', 'hello', 'Hello'),
    ('en', 'goodbye', 'Goodbye');
COMMIT;
SQL

RUN chmod -R a+rwx /home/user

RUN chmod 755 /home/user

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8