FROM ubuntu:22.04

LABEL Author="container-specialist" \
      Description="Prepares initial state with log files and installs pytest"

ENV PYTHONIOENCODING=UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/logs

RUN cat << 'EOF' > /home/user/logs/auth.log
2023-08-01 12:00:00 INFO  Starting service
2023-08-01 12:01:00 ERROR Failed to connect to DB
2023-08-01 12:02:00 INFO  Retrying
2023-08-01 12:03:00 ERROR Timeout reached
EOF

RUN cat << 'EOF' > /home/user/logs/billing.log
2023-08-01 12:00:00 INFO  Starting service
2023-08-01 12:05:00 ERROR Payment gateway unreachable
2023-08-01 12:06:00 INFO  Circuit breaker open
EOF

RUN cat << 'EOF' > /home/user/logs/inventory.log
2023-08-01 12:00:00 INFO  Starting service
2023-08-01 12:04:00 INFO  Inventory synced
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/logs && \
    chmod 644 /home/user/logs/*.log