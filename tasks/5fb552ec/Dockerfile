# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help:
# This container image provides the initial filesystem state for the
# “collect ERROR logs” exercise. It contains the application logs under
# /home/user/app/logs and has pytest installed for the autograder.

LABEL Author="devops-task-preparer"
LABEL Description="Container for ERROR log collection exercise"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/app/logs/old

RUN cat >/home/user/app/logs/auth.log <<'EOF'
[2024-05-01 10:00:00] INFO User login succeeded
[2024-05-01 10:01:00] ERROR Invalid password for user 'bob'
[2024-05-01 10:02:00] ERROR User 'alice' account locked
[2024-05-01 10:03:00] INFO Session ended
[2024-05-01 10:04:00] INFO User logout
EOF

RUN cat >/home/user/app/logs/db.log <<'EOF'
[2024-05-01 12:00:00] INFO Connection pool initialised
[2024-05-01 12:01:00] INFO Query executed successfully
[2024-05-01 12:02:00] INFO Connection closed
EOF

RUN cat >/home/user/app/logs/payment.log <<'EOF'
[2024-05-02 08:00:00] ERROR Payment gateway timeout
[2024-05-02 08:00:01] ERROR Retry attempt failed
[2024-05-02 08:00:02] INFO Payment fallback success
[2024-05-02 08:00:03] INFO Receipt sent
[2024-05-02 08:00:04] ERROR Payment record missing
[2024-05-02 08:00:05] INFO Audit complete
EOF

RUN cat >/home/user/app/logs/old/archive.log <<'EOF'
[2024-04-25 00:00:00] INFO Archival started
[2024-04-25 00:00:01] INFO Reading tables
[2024-04-25 00:00:02] ERROR Disk full during archival
[2024-04-25 00:00:03] INFO Archival aborted
EOF

RUN chmod 0777 /home/user && \
    chmod -R a+r /home/user/app && \
    find /home/user/app -type d -exec chmod a+rx {} \;