FROM ubuntu:22.04

# Labels
LABEL Author="ChatGPT"
LABEL Description="SQLite smoke-test environment with pytest pre-installed."

# Update package index and install required tools
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        sqlite3 \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/dev_data && \
    chmod 0755 /home/user/dev_data

# Build the SQLite database with the prescribed schema & seed data
RUN sqlite3 /home/user/dev_data/api_responses.db <<'SQL'
CREATE TABLE responses(
    id INTEGER PRIMARY KEY,
    endpoint TEXT,
    status_code INTEGER,
    ts TEXT
);
INSERT INTO responses(id, endpoint, status_code, ts) VALUES
    (1, '/v1/accounts', 200, '2023-10-01T10:00:00Z'),
    (2, '/v1/accounts', 500, '2023-10-01T10:01:00Z'),
    (3, '/v1/accounts', 200, '2023-10-01T10:02:00Z'),
    (4, '/v1/payments', 200, '2023-10-01T10:03:00Z');
SQL

# Ensure database file permissions are readable by all but not writable by group/other
RUN chmod 0644 /home/user/dev_data/api_responses.db

# Environment variables
ENV PATH="/usr/local/bin:$PATH"