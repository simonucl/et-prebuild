FROM ubuntu:22.04

# Labels from %labels
LABEL Author="Automated build for deployment-engineering exercise"
LABEL Version="v1.4.0 initial state"

# Base OS packages and Python tooling
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        tar \
        gzip && \
    pip3 install --no-cache-dir pytest

# Create non-privileged user account (UID 1000)
RUN if ! id -u user >/dev/null 2>&1; then useradd -m -u 1000 user; fi

# Ensure home directory exists and is writable
RUN install -d -m 0777 /home/user

# Directory structure
RUN install -d -m 0777 /home/user/app/data && \
    install -d -m 0777 /home/user/app/logs && \
    install -d -m 0777 /home/user/update_scripts && \
    install -d -m 0777 /home/user/backups && \
    install -d -m 0777 /home/user/deployment && \
    install -d -m 0777 /home/user/tmp

# SQLite database initialization
RUN DB_PATH=/home/user/app/data/app.db && \
    sqlite3 "$DB_PATH" <<'SQL_EOF'
CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    name TEXT
);
INSERT INTO users(id, name) VALUES (1, 'Alice');
SQL_EOF
RUN chmod 0666 /home/user/app/data/app.db

# Migration SQL script
RUN cat > /home/user/update_scripts/02_create_release_info.sql <<'SQL_SCRIPT'
CREATE TABLE release_info(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version TEXT NOT NULL,
    deployed_at TEXT DEFAULT CURRENT_TIMESTAMP
);
SQL_SCRIPT
RUN chmod 0666 /home/user/update_scripts/02_create_release_info.sql

# Log files
RUN touch /home/user/app/logs/access.log && \
    touch /home/user/app/logs/error.log && \
    chmod 0666 /home/user/app/logs/access.log /home/user/app/logs/error.log

# Relax permissions
RUN chmod -R a+rwX /home/user

# ENV section
RUN chmod 755 /home/user
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin