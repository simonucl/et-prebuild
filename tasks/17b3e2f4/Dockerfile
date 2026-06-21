FROM ubuntu:22.04

# Author network-task-setup
# Description: Container with pre-populated network diagnostics SQLite DB and pytest for autograding
# Help:
# This container image is prepared for the "gateway failure count" task.
# It contains:
#   • Directories: /home/user/network and /home/user/network/reports
#   • SQLite DB : /home/user/network/conn_logs.db with pre-seeded data
#   • pytest     : for the test harness
# The student must query the DB and write the correct answer to the specified log file.

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip sqlite3 && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/network/reports && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/network && \
    chmod 0755 /home/user/network/reports

RUN sqlite3 /home/user/network/conn_logs.db <<'EOF'
PRAGMA journal_mode = OFF;
CREATE TABLE ping_results (
    id        INTEGER PRIMARY KEY,
    host      TEXT,
    status    TEXT,
    timestamp TEXT
);
INSERT INTO ping_results (id, host, status, timestamp) VALUES
    (1, 'gateway', 'failure', '2023-10-05 00:12:34'),
    (2, 'gateway', 'failure', '2023-10-05 05:45:12'),
    (3, 'gateway', 'success', '2023-10-05 06:00:01'),
    (4, 'gateway', 'failure', '2023-10-05 23:59:59'),
    (5, 'router1', 'failure', '2023-10-05 10:22:11'),
    (6, 'gateway', 'failure', '2023-10-04 20:00:00'),
    (7, 'gateway', 'success', '2023-10-03 08:00:00');
EOF

RUN chmod 0644 /home/user/network/conn_logs.db && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*