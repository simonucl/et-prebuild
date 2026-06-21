FROM ubuntu:22.04

# Install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 777 /home/user

# Create and populate the SQLite database
RUN sqlite3 /home/user/app_release.db <<'SQL'
PRAGMA journal_mode=OFF;
CREATE TABLE IF NOT EXISTS releases(
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    version TEXT    NOT NULL UNIQUE,
    status  TEXT    NOT NULL
);
DELETE FROM releases;
INSERT INTO releases(version, status) VALUES ('v1.0.0', 'deployed');
INSERT INTO releases(version, status) VALUES ('v1.1.0', 'deployed');
SQL

# Ensure the database is writable by the non-root runtime user
RUN chmod 666 /home/user/app_release.db

# Guarantee the confirmation file does not exist at build time
RUN rm -f /home/user/release_log.csv

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin"

# Set working directory
WORKDIR /home/user

# Default command
CMD ["bash", "-c", "echo 'Release-manager exercise container.' && echo \"Run 'bash' to start an interactive shell.\" && exec /bin/bash"]