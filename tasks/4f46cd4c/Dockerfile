FROM ubuntu:22.04

# Help / metadata
# Author: DevOps Task Generator
# Description: Initial state for pipeline log triage assignment

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user

RUN mkdir -p /home/user/app/logs

RUN cat > /home/user/app/logs/pipeline.log <<'EOF'
[2023-09-01 10:00:00] INFO Starting pipeline
[2023-09-01 10:00:01] WARNING Missing optional config value 'threshold', default applied
[2023-09-01 10:00:02] ERROR Failed to connect to database
[2023-09-01 10:00:03] INFO Retrying in 5 seconds
[2023-09-01 10:00:08] INFO Connected after 1 retries
[2023-09-01 10:00:09] WARNING Deprecated API call 'fetch_data_v1'
[2023-09-01 10:00:10] INFO Pipeline finished successfully
EOF

RUN chmod 0644 /home/user/app/logs/pipeline.log

RUN mkdir -p /home/user/app/reports && chmod 0777 /home/user/app/reports

RUN chmod 755 /home/user

ENV LANG=C
ENV LC_ALL=C