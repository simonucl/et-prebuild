FROM ubuntu:22.04

# Help text
# This container provides the starting filesystem state for the
# “error roll-up” task. Three original *.log files are placed under
# /home/user/logs/, and pytest is installed so the grading tests can run.
# No solution artifacts (error_report.txt, error_summary.log, or
# logs_backup.tar.gz) are present.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/logs/app1 && \
    mkdir -p /home/user/logs/app2

RUN cat <<'EOF' > /home/user/logs/app1/server.log
[2023-08-10 10:00:01] INFO  Server started
[2023-08-10 10:05:11] ERROR Failed to connect to DB
[2023-08-10 10:06:43] WARN  Low disk space
[2023-08-10 10:07:02] ERROR User authentication failed
EOF

RUN cat <<'EOF' > /home/user/logs/app1/access.log
127.0.0.1 - - [10/Aug/2023:10:01:00 +0000] "GET /index.html HTTP/1.1" 200 1024
127.0.0.1 - - [10/Aug/2023:10:06:00 +0000] "POST /login HTTP/1.1" 500 2048 ERROR Internal server error
EOF

RUN cat <<'EOF' > /home/user/logs/app2/backend.log
2023-08-10 10:10:00,001 INFO  Job started
2023-08-10 10:12:22,333 ERROR NullPointer at worker.go:88
2023-08-10 10:13:30,555 INFO  Job finished
EOF

RUN chmod -R a+r /home/user/logs

RUN chmod 755 /home/user

LABEL Author="Auto-generated for error roll-up task"
LABEL Description="Base image with pre-populated log files and pytest installed."