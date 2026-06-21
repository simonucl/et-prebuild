FROM ubuntu:22.04

# Install runtime tooling
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        gawk \
        sed && \
    pip3 install --no-cache-dir pytest

# Create initial file set - Base directories
RUN mkdir -p /home/user/logs && \
    mkdir -p /home/user/config

# Create system.log with the required contents
RUN cat > /home/user/logs/system.log <<'EOF'
2023-05-01 10:15:23 INFO  Startup complete
2023-05-01 10:15:24 ERROR [E101] Failed to load module alpha
2023-05-01 10:15:25 WARN  Low memory
2023-05-01 10:15:26 ERROR [E102] Connection timeout
2023-05-01 10:15:27 INFO  Health check passed
2023-05-01 10:15:28 ERROR [E101] Failed to load module alpha
2023-05-01 10:15:29 ERROR [E103] Disk full
EOF

# Create app.conf with the required initial state
RUN cat > /home/user/config/app.conf <<'EOF'
#diagnostics=false
loglevel=INFO
path=/var/app/
EOF

# Make sure the agent can write
# Give world-write permissions so the non-privileged runtime user can
# create /home/user/diagnostics and edit files as required.
RUN chmod -R a+rwX /home/user

# Environment variables
ENV PYTHONIOENCODING=UTF-8

# Default command
CMD echo "Container for diagnostics task. No default runtime command."