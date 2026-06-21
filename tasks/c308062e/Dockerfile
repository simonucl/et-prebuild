# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Label converted from %labels
LABEL Author="ChatGPT – Apptainer setup for localisation task"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/projects/i18n/backups

RUN sqlite3 /home/user/projects/i18n/app_translations.db <<'SQL'
PRAGMA journal_mode = WAL;
CREATE TABLE translations (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    language   TEXT NOT NULL,
    key        TEXT NOT NULL,
    value      TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

INSERT INTO translations (id, language, key, value, updated_at) VALUES
    (1, 'en', 'welcome_message',  'Welcome',    '2023-01-10 12:00:00'),
    (2, 'fr', 'welcome_message',  'Bienvenue',  '2023-01-10 12:00:00'),
    (3, 'de', 'welcome_message',  'Willkommen', '2023-01-10 12:00:00'),
    (4, 'fr', 'help_link',        'Aide',       '2023-01-15 09:00:00'),
    (5, 'de', 'deprecated_notice','Veraltet',   '2023-01-20 15:00:00');
SQL

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked chmod 0666 /home/user/projects/i18n/app_translations.db && \
    chmod 0777 /home/user/projects/i18n/backups && \
    chmod 0755 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*