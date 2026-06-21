# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# This container provides the initial state for the localization database task.
# - SQLite database with English strings is ready at /home/user/project/i18n/strings.db
# - Pytest is installed for automated grading.

ENV DEBIAN_FRONTEND=noninteractive

# 1. Install required system packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 2. Install Python test dependency
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# 3. Create user and prepare initial project directory structure
RUN useradd -m -d /home/user -s /bin/bash user && \
    mkdir -p /home/user/project/i18n && \
    chmod 755 /home/user /home/user/project /home/user/project/i18n || true && \
    chown -R user:user /home/user

# 4. Create and populate the initial SQLite database
RUN cat <<'SQL' | sqlite3 /home/user/project/i18n/strings.db
CREATE TABLE translations (
    id     INTEGER PRIMARY KEY,
    lang   TEXT NOT NULL,
    key    TEXT NOT NULL,
    value  TEXT NOT NULL
);
INSERT INTO translations (id, lang, key, value) VALUES
    (1, 'en', 'greeting', 'Hello'),
    (2, 'en', 'farewell', 'Bye');
SQL

RUN chmod 664 /home/user/project/i18n/strings.db && \
    chown user:user /home/user/project/i18n/strings.db

# 5. Ensure that no update log exists at build time
RUN rm -f /home/user/project/update_log.txt

# Environment variables
ENV PATH="/usr/local/bin:${PATH}"

USER user
WORKDIR /home/user

CMD ["bash"]