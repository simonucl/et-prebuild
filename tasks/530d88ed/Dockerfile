FROM ubuntu:22.04

# Install required packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        sqlite3 \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Prepare filesystem layout
RUN mkdir -p /home/user/configs

# Create SQLite database with table and seed data
RUN DB_PATH="/home/user/configs/security_audit.db" && \
    sqlite3 "${DB_PATH}" <<'EOF'
PRAGMA journal_mode=OFF;
CREATE TABLE services (
    id     INTEGER PRIMARY KEY,
    name   TEXT NOT NULL,
    status TEXT NOT NULL
);
INSERT INTO services (id, name, status) VALUES
    (1, 'sshd', 'enabled'),
    (2, 'cron', 'enabled'),
    (3, 'cups', 'disabled'),
    (4, 'ufw',  'enabled');
EOF

# Set permissions
RUN chmod 755 /home/user && \
    chmod 755 /home/user/configs && \
    chmod 644 /home/user/configs/security_audit.db

# Environment settings
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Labels
LABEL Author="Generated definition file for enabled_services CSV task"

# Default run behavior
CMD echo "Container for the enabled_services CSV task." && \
    echo "Use this environment to solve the exercise."