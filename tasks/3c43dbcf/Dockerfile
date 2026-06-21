FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/diag

RUN cat >/home/user/diag/cpu_usage.log <<'EOF'
2023-07-15T10:00:00 12
2023-07-15T10:05:00 18
2023-07-15T10:10:00 20
2023-07-15T10:15:00 25
EOF

RUN cat >/home/user/diag/mem_usage.log <<'EOF'
2023-07-15T10:00:00 2048
2023-07-15T10:05:00 2100
2023-07-15T10:10:00 2150
2023-07-15T10:15:00 2200
EOF

RUN chmod 777 /home/user/diag && \
    chmod 644 /home/user/diag/*.log && \
    chmod 755 /home/user

LABEL Author="Generated for performance-log merging exercise"