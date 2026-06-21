# syntax=docker/dockerfile:1
# Converted from Apptainer definition file
FROM ubuntu:22.04

# Help text
# This container is prepared for the log-parsing automation task.
# It includes:
#   • Two raw log files in /home/user/workflow_logs/
#   • Python 3 with pytest
#   • Common CLI utilities (grep, awk, sed, jq, tar, etc.)
#   • Nothing else in /home/user/workflow_logs/ besides app.log and access.log

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        grep \
        gawk \
        sed \
        coreutils \
        tar && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/workflow_logs

RUN cat <<'EOF' > /home/user/workflow_logs/app.log
2023-08-01 09:15:04,123 INFO  Workflow started by user=alice id=WF1001
2023-08-01 09:16:10,456 ERROR Step 1 failed with code=E42
2023-08-01 09:16:20,789 INFO  Retrying step 1 attempt=2
2023-08-01 09:16:25,012 ERROR Step 1 failed with code=E42
2023-08-01 10:03:55,334 INFO  Workflow resumed id=WF1001
2023-08-01 10:04:12,667 ERROR Step 2 failed with code=E17
2023-08-01 11:22:33,890 WARNING Deprecated API used by user=bob
2023-08-01 11:45:01,101 ERROR Step 3 failed with code=E99
EOF

RUN cat <<'EOF' > /home/user/workflow_logs/access.log
192.168.0.11 - - [01/Aug/2023:09:15:04 +0000] "POST /api/workflow HTTP/1.1" 200 523
192.168.0.11 - - [01/Aug/2023:09:16:10 +0000] "GET /api/workflow/step1 HTTP/1.1" 500 214
172.16.4.15 - - [01/Aug/2023:09:16:25 +0000] "GET /api/workflow/step1 HTTP/1.1" 500 214
192.168.0.11 - - [01/Aug/2023:10:04:12 +0000] "GET /api/workflow/step2 HTTP/1.1" 500 214
10.0.0.5     - - [01/Aug/2023:11:45:01 +0000] "GET /api/workflow/step3 HTTP/1.1" 500 214
172.16.4.15 - - [01/Aug/2023:11:45:02 +0000] "GET /favicon.ico HTTP/1.1" 404 88
EOF

RUN chmod 0755 /home/user && \
    chmod 0755 /home/user/workflow_logs && \
    chmod 0644 /home/user/workflow_logs/*.log

# Labels
LABEL Author="AutomatedSetup"
LABEL Description="Environment for workflow log parsing task with pytest pre-installed."