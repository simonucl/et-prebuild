# Author: AutomationSetup  
# Description: Environment for SQLite inventory summarization task

FROM ubuntu:22.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

RUN mkdir -p /home/user/data && \
    mkdir -p /home/user/output && \
    chmod 0777 /home/user/output

RUN sqlite3 /home/user/data/warehouse.db <<'SQL_END'
PRAGMA journal_mode=OFF;
CREATE TABLE inventory (
    id   INTEGER PRIMARY KEY,
    item TEXT    NOT NULL,
    qty  INTEGER NOT NULL
);
INSERT INTO inventory (id, item, qty) VALUES
    (1, 'bolts',   10),
    (2, 'nuts',    12),
    (3, 'washers',  8),
    (4, 'screws',   7),
    (5, 'spacers',  5);
SQL_END

RUN chmod 0644 /home/user/data/warehouse.db && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Runscript equivalent:
# echo "Container for the inventory summarization task."
# echo "Use an interactive shell or execute your commands directly."