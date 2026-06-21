FROM ubuntu:22.04

# Install required system packages
RUN set -e && \
    apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Prepare initial filesystem layout
RUN mkdir -p /home/user/ci_cd_poc

# Create SQLite database with initial state
RUN sqlite3 /home/user/ci_cd_poc/pipelines.db <<'EOF'
CREATE TABLE builds (
    id INTEGER PRIMARY KEY,
    status TEXT,
    started_at TEXT
);

INSERT INTO builds (id, status, started_at) VALUES
    (1, 'success', '2023-01-01T10:00:00Z'),
    (2, 'failed',  '2023-01-02T11:00:00Z'),
    (3, 'success', '2023-01-03T12:00:00Z');
EOF

# Permissions
RUN chmod 777 /home/user/ci_cd_poc && \
    chmod 666 /home/user/ci_cd_poc/pipelines.db && \
    mkdir -p /home/user && chmod 755 /home/user

# Labels
LABEL Author="Automated Container Prep"
LABEL Description="Initial state for CI/CD SQLite assignment with pytest installed"