FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state for the task
RUN mkdir -p /home/user/deployment && \
    chmod 777 /home/user /home/user/deployment

# Create the provided server.log with exact content
RUN cat > /home/user/deployment/server.log <<'EOF'
[2024-05-01 10:01:03] STARTUP complete
[2024-05-01 10:02:17] UPDATED service-A to v1.4.2
[2024-05-01 10:03:08] Health-check passed
[2024-05-01 10:05:44] UPDATED service-B to v3.2.1
[2024-05-01 10:07:09] NOTICE scaling event
[2024-05-01 10:10:22] UPDATED cache-layer configuration
[2024-05-01 10:12:56] INFO background job started
[2024-05-01 10:15:31] UPDATED database schema migration
[2024-05-01 10:18:47] WARN high memory usage
[2024-05-01 10:20:00] COMPLETED rollout script
[2024-05-01 10:21:15] UPDATED monitoring alerts
[2024-05-01 10:22:59] SHUTDOWN initiated
EOF

# Make sure the log file is writable by any user
RUN chmod 666 /home/user/deployment/server.log

# Set environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Set default command
CMD ["echo", "Deployment log counting container."]