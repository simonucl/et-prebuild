# Author: shell-scripting-log-task
# Description: Environment for the 'Shell-scripting automation for a log analyst' task
# Help:
# This container image provides the pre-populated HTTP log files and
# directory structure required for the “Shell-scripting automation for a
# log analyst” exercise.
# It also includes pytest so that the grading harness can execute tests.

FROM ubuntu:22.04

RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data/logs && \
    mkdir -p /home/user/data/reports && \
    mkdir -p /home/user/bin

RUN cat >/home/user/data/logs/app1.log <<'EOF'
[2023-01-01 10:00:01] "GET /index.html" 200
[2023-01-01 10:00:02] "GET /login" 404
[2023-01-01 10:00:03] "POST /api/data" 500
[2023-01-01 10:00:04] "GET /about" 200
EOF

RUN cat >/home/user/data/logs/app2.log <<'EOF'
[2023-01-02 11:05:05] "GET /" 200
[2023-01-02 11:05:06] "GET /doesnotexist" 404
[2023-01-02 11:05:07] "GET /" 200
EOF

RUN cat >/home/user/data/logs/app3.log <<'EOF'
[2023-01-03 09:15:05] "POST /submit" 500
[2023-01-03 09:15:06] "GET /home" 200
[2023-01-03 09:15:07] "GET /contact" 200
[2023-01-03 09:15:08] "GET /notfound" 404
EOF

RUN chmod 644 /home/user/data/logs/*.log && \
    chmod 755 /home/user/data/logs && \
    chmod 0777 /home/user/data/reports && \
    chmod 0777 /home/user/bin && \
    chmod 755 /home/user && \
    chmod 755 /home/user/data && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/home/user/bin:${PATH}"
ENV LC_ALL=C.UTF-8