FROM ubuntu:22.04

# Install Python and pytest (for the automated checker)
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare filesystem needed for the "ERROR line extraction" task
# Ensure the target directory structure exists
RUN mkdir -p /home/user/app/logs

# Create the canonical /home/user/app/logs/app.log file
RUN cat >/home/user/app/logs/app.log <<'EOF'
2023-08-20 11:37:02 INFO Starting service
2023-08-20 11:37:05 WARN Config file not found, using defaults
2023-08-20 11:37:10 ERROR Failed to connect to database
2023-08-20 11:37:12 INFO Retrying connection
2023-08-20 11:37:15 ERROR Failed to connect to database
2023-08-20 11:37:18 INFO Giving up after 3 retries
2023-08-20 11:37:20 ERROR Service terminated unexpectedly
2023-08-20 11:37:22 INFO Shutdown complete
EOF

# Permissions: directory must be writable by the (non-root) runtime user
# The log file itself only needs read permission; leave it world-readable
RUN chmod 0777 /home/user/app/logs && \
    chmod 0644 /home/user/app/logs/app.log && \
    chmod 755 /home/user

# Labels
LABEL Author="DevOps Challenge Generator"
LABEL Description="Container set-up for the ERROR extraction task (includes pytest)."

# Default command
CMD ["echo", "Docker environment ready for the ERROR extraction task."]