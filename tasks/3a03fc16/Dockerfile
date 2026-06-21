FROM ubuntu:22.04

# Base tools + Python & pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Directory structure for the exercise
RUN mkdir -p /home/user/microservices/logs

# Make the parent folders writable so that the unprivileged runtime
# user can create additional directories/files (reports/, archive/, …)
RUN chmod 0777 /home/user && \
    chmod 0777 /home/user/microservices

# Pre-populated log files - serviceA.log
RUN cat > /home/user/microservices/logs/serviceA.log <<'EOF'
2023-09-14 10:15:32 INFO Starting service
2023-09-14 10:17:02 ERROR Failed to connect to DB
2023-09-14 11:05:12 WARNING Low memory
2023-09-15 09:45:00 INFO Health check passed
2023-09-15 12:08:45 ERROR Timeout while processing request
2023-09-16 13:00:00 INFO Shutdown signal received
EOF

# Pre-populated log files - serviceB.log
RUN cat > /home/user/microservices/logs/serviceB.log <<'EOF'
2023-09-13 08:00:00 INFO Starting service
2023-09-13 08:30:21 WARNING Cache miss
2023-09-14 09:00:02 ERROR Unhandled exception
2023-09-15 10:05:05 ERROR Null pointer
2023-09-16 11:11:11 WARNING High latency
2023-09-16 12:00:00 INFO Rolling update completed
EOF

# Pre-populated log files - serviceC.log
RUN cat > /home/user/microservices/logs/serviceC.log <<'EOF'
2023-09-14 14:22:10 INFO Init
2023-09-14 14:23:00 WARNING Deprecated API
2023-09-15 16:45:30 ERROR Disk full
2023-09-15 18:00:00 ERROR Permission denied
2023-09-16 19:30:30 WARNING Configuration reload
2023-09-16 20:00:00 INFO Done
EOF

# Ensure log files are readable
RUN chmod 0644 /home/user/microservices/logs/*.log

# Environment settings
ENV PATH="/usr/local/bin:${PATH}"