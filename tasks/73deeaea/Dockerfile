# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# --------------------------------------------------------------------- #
# System packages                                                       #
# --------------------------------------------------------------------- #
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        sqlite3 \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------------------- #
# Python tooling                                                        #
# --------------------------------------------------------------------- #
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# --------------------------------------------------------------------- #
# Directory structure required by the task                              #
# --------------------------------------------------------------------- #
RUN mkdir -p /home/user/projects/loc/db && \
    mkdir -p /home/user/projects/loc/report && \
    chmod 700 /home/user/projects/loc/db && \
    chmod 700 /home/user/projects/loc/report

# --------------------------------------------------------------------- #
# Pre-populated SQLite database                                         #
# --------------------------------------------------------------------- #
RUN sqlite3 /home/user/projects/loc/db/translations.db <<'SQLINIT'
PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;
CREATE TABLE strings(
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    key   TEXT UNIQUE NOT NULL,
    en    TEXT NOT NULL,
    es    TEXT
);
INSERT INTO strings(key, en, es) VALUES
    ('hello_msg',   'Hello!',  '¡Hola!'),
    ('goodbye_msg', 'Goodbye!', NULL);
COMMIT;
SQLINIT

# --------------------------------------------------------------------- #
# Environment                                                           #
# --------------------------------------------------------------------- #
RUN chmod 755 /home/user
ENV LC_ALL=C

# --------------------------------------------------------------------- #
# Metadata                                                              #
# --------------------------------------------------------------------- #
LABEL Author="example" \
      Description="Localization database update task – initial state setup"

# Default command (equivalent to Apptainer runscript)
CMD ["/bin/bash"]