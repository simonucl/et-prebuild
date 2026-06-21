FROM ubuntu:22.04

# Help / metadata
# Author: ChatGPT – generated
# Description: Container for the authentication-log incident-response task with pre-populated SQLite database and pytest installed.

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/ir_breach && \
    chmod 755 /home/user && \
    chmod 755 /home/user/ir_breach

RUN cat > /tmp/init.sql <<'EOF'
CREATE TABLE auth_log(
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    username TEXT,
    src_ip TEXT,
    action TEXT
);

INSERT INTO auth_log (id, timestamp, username, src_ip, action) VALUES
  (1, '2023-08-10 05:03:11', 'alice',   '192.168.1.20',   'SUCCESS'),
  (2, '2023-08-10 05:05:43', 'root',    '203.0.113.45',   'FAIL'),
  (3, '2023-08-10 05:05:55', 'root',    '203.0.113.45',   'FAIL'),
  (4, '2023-08-10 05:06:12', 'root',    '203.0.113.45',   'FAIL'),
  (5, '2023-08-10 05:07:01', 'bob',     '198.51.100.23',  'FAIL'),
  (6, '2023-08-10 05:08:47', 'charlie', '192.168.1.100',  'SUCCESS'),
  (7, '2023-08-10 05:09:10', 'root',    '203.0.113.45',   'SUCCESS'),
  (8, '2023-08-10 05:10:42', 'bob',     '198.51.100.23',  'FAIL'),
  (9, '2023-08-10 05:11:33', 'david',   '203.0.113.78',   'FAIL'),
  (10,'2023-08-10 05:12:00', 'eve',     '198.51.100.23',  'SUCCESS');
EOF

RUN sqlite3 /home/user/ir_breach/breach.db < /tmp/init.sql && \
    chmod 644 /home/user/ir_breach/breach.db && \
    rm /tmp/init.sql

LABEL Author="ChatGPT – generated"
LABEL Description="Container for the authentication-log incident-response task with pre-populated SQLite database and pytest installed."