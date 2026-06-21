# Author="Apptainer Task Setup"
# Description="Container prepared for SSH key rotation verification exercise."

FROM ubuntu:22.04

ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    python3 -m pip install --no-cache-dir pytest

RUN mkdir -p /home/user/logs

RUN cat > /home/user/logs/credential_events_20240115.log <<'EOF'
2024-01-15T14:45:30Z,alice,OLD_KEY
2024-01-15T14:50:42Z,bob,OLD_KEY
2024-01-15T14:59:59Z,alice,NEW_KEY
2024-01-15T15:12:04Z,alice,OLD_KEY
2024-01-15T15:30:10Z,carol,NEW_KEY
2024-01-15T16:45:19Z,bob,OLD_KEY
2024-01-15T16:50:02Z,carol,NEW_KEY
2024-01-15T17:01:54Z,alice,OLD_KEY
2024-01-15T17:15:00Z,carol,NEW_KEY
EOF

RUN chmod 755 /home/user/logs && \
    chmod 644 /home/user/logs/credential_events_20240115.log

RUN if [ -e /home/user/rotation_report ]; then rm -rf /home/user/rotation_report; fi