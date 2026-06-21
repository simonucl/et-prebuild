FROM ubuntu:22.04

# Help/metadata
# Author: quick-scan exercise
# Description: Initial state for “one-off security-style scan” task.

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip install --no-cache-dir pytest && \
    mkdir -p /home/user/app/logs && \
    chmod 0777 /home/user

RUN cat >/home/user/app/logs/latest.log <<'EOF'
[2024-05-24 10:11:12] INFO  Starting service
[2024-05-24 10:11:13] ERROR Failed to connect
[2024-05-24 10:11:14] TRACEBACK: ConnectionError at service.main
[2024-05-24 10:11:15] INFO  Retrying
[2024-05-24 10:11:16] TRACEBACK: TimeoutError at service.helper
[2024-05-24 10:11:17] INFO  Service recovered
[2024-05-24 10:11:18] DEBUG Heartbeat OK
[2024-05-24 10:11:19] TRACEBACK: UnknownError at service.dispatcher
[2024-05-24 10:11:20] INFO  Shutdown complete
EOF

RUN chmod 644 /home/user/app/logs/latest.log && \
    chmod 755 /home/user/app && \
    chmod 755 /home/user/app/logs

LABEL Author="quick-scan exercise"
LABEL Description="Initial state for one-off security-style scan task."