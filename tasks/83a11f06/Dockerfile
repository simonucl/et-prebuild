# Author: devops@task
# Description: Base container for log-processing task with initial log file and pytest installed.

FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python-is-python3 \
        sqlite3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pytest

RUN mkdir -p /home/user && mkdir -p /home/user/logs

RUN cat > /home/user/logs/app.log <<'EOF'
2024-04-01 10:15:32 INFO  Application started
2024-04-01 10:16:45 ERROR Failed to connect to database
2024-04-01 10:17:02 WARN  Retrying connection
2024-04-01 10:17:10 INFO  Connected successfully
2024-04-01 10:18:21 ERROR Timeout during query
2024-04-01 10:19:01 INFO  Request completed
2024-04-01 10:20:11 INFO  Shutdown complete
EOF

RUN chmod 0777 /home/user/logs && \
    chmod 0644 /home/user/logs/app.log && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:$PATH

LABEL Author="devops@task"
LABEL Description="Base container for log-processing task with initial log file and pytest installed."