FROM ubuntu:22.04

# Help / metadata
LABEL Author="FinOps-Exercise"
LABEL Description="Container for FinOps analyst SQLite summation exercise"

# Install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        sqlite3 \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create directory
RUN mkdir -p /home/user/finops && \
    chmod 0755 /home/user/finops

# Create SQLite database using heredoc
RUN sqlite3 /home/user/finops/cloud_spend.db <<'EOF'
CREATE TABLE usage(
    id      INTEGER PRIMARY KEY,
    service TEXT,
    month   TEXT,
    cost    REAL
);
INSERT INTO usage (id, service, month, cost) VALUES
    (1, 'Compute Engine', '2023-07', 523.23),
    (2, 'Cloud Storage',  '2023-07', 123.45),
    (3, 'BigQuery',       '2023-07', 300.00),
    (4, 'Compute Engine', '2023-06', 200.00),
    (5, 'BigQuery',       '2023-07',  77.89);
EOF

# Fix DB permissions
RUN chmod 0644 /home/user/finops/cloud_spend.db

# Environment setup
RUN chmod 755 /home/user
ENV PATH="/usr/bin:$PATH"
ENV PYTHONUNBUFFERED=1