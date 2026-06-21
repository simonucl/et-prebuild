FROM ubuntu:22.04

# Help / labels
LABEL Author="Mobile Build Audit Setup"
LABEL Description="Pre-provisioned environment for the mobile build audit task with pytest installed."

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip sqlite3 && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/mobile_pipelines/report

RUN cat <<'SQL' | sqlite3 /home/user/mobile_pipelines/builds.db
PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;
CREATE TABLE builds (
    id            INTEGER PRIMARY KEY,
    commit_hash   TEXT    NOT NULL,
    status        TEXT    NOT NULL,
    duration_sec  INTEGER NOT NULL,
    timestamp     TEXT    NOT NULL
);
CREATE TABLE artifacts (
    id            INTEGER PRIMARY KEY,
    build_id      INTEGER NOT NULL,
    artifact_name TEXT    NOT NULL,
    size_kb       INTEGER NOT NULL
);
INSERT INTO builds (id, commit_hash, status, duration_sec, timestamp) VALUES
    (1, 'a1b2c3d4', 'SUCCESS', 320, '2023-09-01T12:01:30Z'),
    (2, 'e5f6g7h8', 'FAILED', 150, '2023-09-02T14:22:10Z'),
    (3, 'i9j0k1l2', 'SUCCESS', 287, '2023-09-03T09:47:55Z');
INSERT INTO artifacts (id, build_id, artifact_name, size_kb) VALUES
    (1, 1, 'app-release.apk', 20480),
    (2, 1, 'symbols.zip',     5120),
    (3, 2, 'crash-log.txt',   12),
    (4, 3, 'app-release.apk', 20512);
COMMIT;
SQL

RUN cat <<'EOF' > /home/user/mobile_pipelines/report/build_summary.log
Build Summary Report

Commit Hash | Status   | Artifact Count
----------------------------------------
a1b2c3d4     | SUCCESS  | 2
e5f6g7h8     | FAILED   | 1
i9j0k1l2     | SUCCESS  | 1
EOF

RUN chmod -R a+rX /home/user