FROM ubuntu:22.04

# Install required packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 && \
    pip install --no-cache-dir pytest

# Prepare directory structure
RUN mkdir -p /home/user && \
    chmod 777 /home/user && \
    mkdir -p /home/user/projects/loc/db && \
    chmod -R 777 /home/user/projects

# Create and seed the SQLite database
RUN sqlite3 /home/user/projects/loc/db/translations.db <<'SQL'
PRAGMA journal_mode=OFF;
PRAGMA synchronous=OFF;

CREATE TABLE translations (
    id          INTEGER PRIMARY KEY,
    locale      TEXT,
    key         TEXT,
    value       TEXT,
    updated_at  TEXT
);

INSERT INTO translations (id, locale, key, value, updated_at) VALUES
    (1, 'en', 'welcome', 'Welcome', '2023-01-01'),
    (2, 'en', 'logout',  'Logout',  '2023-01-01'),
    (3, 'es', 'welcome', 'Bienvenido', '2023-01-01'),
    (4, 'es', 'logout',  'Cerrar sesión', '2023-01-01');
SQL

# Set database permissions
RUN chmod 666 /home/user/projects/loc/db/translations.db

# Clean up to keep image size small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set permissions and environment variables
RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8