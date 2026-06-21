# Author="Task setup for quick compliance spot-check exercise"

FROM ubuntu:22.04

ENV PYTHONUNBUFFERED=1

RUN chmod 755 /home/user || true

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/logs

RUN cat <<'EOF' > /home/user/logs/app_2023-09-15.log
2023-09-15 09:01:02 [INFO] Startup complete
2023-09-15 09:05:33 [ERROR] Failed to connect to database
2023-09-15 09:06:01 [ERROR] Authentication service unavailable
2023-09-15 09:10:45 [WARN] High memory usage detected
2023-09-15 09:15:12 [ERROR] Disk write failure
2023-09-15 09:25:37 [ERROR] Network timeout
2023-09-15 09:40:22 [INFO] Scheduled job started
2023-09-15 09:45:02 [ERROR] Cache synchronization failed
2023-09-15 10:00:15 [ERROR] Unexpected null pointer exception
2023-09-15 10:30:00 [INFO] Daily rotation complete
2023-09-15 10:45:23 [ERROR] Backup process interrupted
EOF

RUN chmod 0777 /home/user && \
    chmod 0755 /home/user/logs && \
    chmod 0644 /home/user/logs/app_2023-09-15.log && \
    rm -rf /home/user/compliance