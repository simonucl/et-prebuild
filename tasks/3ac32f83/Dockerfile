FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state
RUN mkdir -p /home/user/support/logs && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/support && \
    chmod 0755 /home/user/support/logs

# Populate the application log
RUN cat > /home/user/support/logs/app.log <<'EOF'
2023-10-15 10:15:42,123 INFO  main      REQ-000101 Starting service
2023-10-15 10:16:05,675 ERROR main      REQ-000102 Failed to connect to database
2023-10-15 10:16:07,101 WARN  worker-1  REQ-000103 Retrying
2023-10-15 10:16:10,333 ERROR worker-1  REQ-000104 Timeout reached during operation
2023-10-15 10:16:12,890 INFO  main      REQ-000105 Health check passed
2023-10-15 10:16:15,200 ERROR worker-2  REQ-000106 Null pointer exception
2023-10-15 10:16:16,400 INFO  worker-2  REQ-000107 Shutdown complete
EOF

RUN chmod 0644 /home/user/support/logs/app.log

# Environment adjustments
RUN chmod 755 /home/user

LABEL Author="error-diagnostics-setup"