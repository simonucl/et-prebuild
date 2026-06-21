FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        sqlite3 \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/ir_case && \
    chmod 0777 /home/user/ir_case

RUN sqlite3 /home/user/ir_case/logs.db <<'SQL_EOF'
CREATE TABLE auth(
    id     INTEGER PRIMARY KEY,
    ts     TEXT,
    user   TEXT,
    status TEXT
);
INSERT INTO auth VALUES
    (1,'2023-08-01 11:23:31','alice','OK'),
    (2,'2023-08-01 11:24:02','bob','FAIL'),
    (3,'2023-08-01 11:25:15','charlie','FAIL'),
    (4,'2023-08-01 11:26:45','alice','FAIL'),
    (5,'2023-08-01 11:28:17','dave','OK'),
    (6,'2023-08-01 11:30:00','charlie','FAIL'),
    (7,'2023-08-01 11:32:12','eve','FAIL'),
    (8,'2023-08-01 11:34:05','bob','OK'),
    (9,'2023-08-01 11:35:19','frank','FAIL');
SQL_EOF

RUN chmod 0644 /home/user/ir_case/logs.db && \
    rm -f /home/user/ir_case/logs.db-shm /home/user/ir_case/logs.db-wal || true

ENV LANG=C
ENV LC_ALL=C
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Author incident-responder exercise container
# Description Container that sets up the initial state for the failed-login incident response task.