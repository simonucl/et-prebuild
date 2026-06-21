FROM ubuntu:22.04

# Install required system packages and Python dependencies
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        sqlite3 \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directory structure
RUN mkdir -p /home/user/security_scans && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/security_scans

# Build the legacy database with the required schema and rows
RUN sqlite3 /home/user/security_scans/scan_results_v1.db <<'SQL'
CREATE TABLE vulnerabilities (
    id   INTEGER PRIMARY KEY,
    host TEXT,
    port INTEGER,
    vuln TEXT
);
INSERT INTO vulnerabilities (id, host, port, vuln) VALUES
    (1, '192.168.0.5', 22,  'OpenSSH 7.2p2 outdated'),
    (2, '192.168.0.18', 445, 'SMB v1 enabled'),
    (3, '10.0.0.7', 80,  'Apache 2.2 directory listing');
SQL

RUN chmod 0666 /home/user/security_scans/scan_results_v1.db

# Set environment variables
ENV PYTHONUSERBASE=/tmp/.pyusr
ENV PATH="$PYTHONUSERBASE/bin:$PATH"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8