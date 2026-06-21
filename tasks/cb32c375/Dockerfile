FROM ubuntu:22.04

# Install required packages.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        sqlite3 \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test-suite that will be provided at run-time.
RUN pip3 install --no-cache-dir pytest

# Prepare initial forensic evidence database at /home/user/source.db
RUN mkdir -p /home/user && \
    chmod 0755 /home/user

RUN cat >/tmp/create_source.sql <<'EOF'
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE network_logs(
  id INTEGER PRIMARY KEY,
  timestamp TEXT,
  src_ip TEXT,
  dest_ip TEXT,
  action TEXT
);
INSERT INTO network_logs VALUES(1,'2023-06-01T12:00:00Z','10.0.0.5','192.168.1.20','ALLOW');
INSERT INTO network_logs VALUES(2,'2023-06-01T12:05:00Z','10.0.0.5','172.16.0.8','ALLOW');
INSERT INTO network_logs VALUES(3,'2023-06-01T12:10:00Z','10.0.0.10','192.168.1.21','DENY');
INSERT INTO network_logs VALUES(4,'2023-06-01T12:15:00Z','10.0.0.15','192.168.1.22','ALLOW');
INSERT INTO network_logs VALUES(5,'2023-06-01T12:20:00Z','10.0.0.20','192.168.1.23','DENY');
COMMIT;
EOF

RUN sqlite3 /home/user/source.db < /tmp/create_source.sql && \
    rm -f /tmp/create_source.sql

# Ensure the database is readable by any user inside the container.
RUN chmod 0644 /home/user/source.db

# Environment variables
ENV LANG=C
ENV LC_ALL=C

# Set working directory
WORKDIR /home/user

CMD ["echo", "SQLite migration container ready. Use 'docker exec' to run commands inside."]