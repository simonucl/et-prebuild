# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text
# This container image provides the initial state for the SQLite
# backup-administration task. It includes:
#   - /home/user/databases/warehouse.db with the required schema/data
#   - An empty /home/user/backups directory (permissions 755)
#   - Python, sqlite3, and pytest pre-installed
# No backup artefacts are present; the student is expected to create them.

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -u 1000 -s /bin/bash user; \
    fi

RUN mkdir -p /home/user && \
    chown -R root:root /home/user && \
    chmod 755 /home/user

RUN mkdir -p /home/user/databases && \
    chmod 755 /home/user/databases

RUN cat <<'SQL' | sqlite3 /home/user/databases/warehouse.db
CREATE TABLE products(
    id    INTEGER PRIMARY KEY,
    name  TEXT,
    stock INTEGER
);
INSERT INTO products(id,name,stock) VALUES
    (1,'wrench',42),
    (2,'hammer',17),
    (3,'screwdriver',58);
SQL

RUN chmod 644 /home/user/databases/warehouse.db

RUN mkdir -p /home/user/backups && \
    chmod 755 /home/user/backups

LABEL Author="backup-task-preparer"
LABEL Description="Environment for SQLite backup task with pytest installed"

CMD ["/bin/bash"]