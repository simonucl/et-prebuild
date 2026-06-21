FROM ubuntu:22.04

# Basic tooling for Python and testing
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    python3 -m pip install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare directory structure
RUN mkdir -p /home/user/monitoring/logs && \
    mkdir -p /home/user/monitoring/alerts

# Seed application log with historical entries
RUN cat > /home/user/monitoring/logs/service.log <<'EOF'
2023-11-01 13:59:59 INFO Service starting
2023-11-01 14:01:12 ERROR Connection lost to DB
2023-11-01 14:05:00 INFO Attempting reconnect
2023-11-01 14:06:47 ERROR Connection lost to DB
2023-11-01 14:50:30 INFO Reconnected to DB
2023-11-01 15:02:03 ERROR Timeout while reading from socket
2023-11-01 15:05:17 WARN High memory usage detected
2023-11-01 15:12:29 ERROR Timeout while reading from socket
2023-11-01 15:30:45 ERROR Timeout while reading from socket
2023-11-01 15:45:00 INFO Memory usage back to normal
2023-11-01 16:00:01 INFO Scheduled report generated
2023-11-01 16:01:02 ERROR Failed to send notification
2023-11-01 16:05:18 ERROR Failed to send notification
2023-11-01 16:10:59 ERROR Failed to send notification
2023-11-01 16:30:00 INFO Service health check passed
EOF

# Permissions so container user can read/write logs and alerts
RUN chmod -R a+rwX /home/user/monitoring && \
    chmod 755 /home/user

# Environment variables
ENV PYTHONUNBUFFERED=1

# Labels
LABEL Author="On-Call Monitoring Scenario"
LABEL Description="Container with pre-seeded service log for monitoring exercise."