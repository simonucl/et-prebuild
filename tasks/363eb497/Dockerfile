FROM ubuntu:22.04

# Author: dev
# Description: Environment for the log-triage exercise (error summary task)

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/pipeline

RUN cat > /home/user/pipeline/app.log <<'EOF'
[2023-11-10 10:01:02] INFO  Starting job
[2023-11-10 10:01:03] ERROR [ERR1001] Failed to connect to DB
[2023-11-10 10:01:04] WARN  Slow response
[2023-11-10 10:01:05] ERROR [ERR1002] Timeout in service
[2023-11-10 10:01:06] ERROR [ERR1001] Failed to connect to DB
[2023-11-10 10:01:07] ERROR [ERR1003] Null pointer exception
[2023-11-10 10:01:08] INFO  Job completed
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/pipeline && \
    chmod 644 /home/user/pipeline/app.log && \
    rm -f /home/user/pipeline/error_summary.log

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1