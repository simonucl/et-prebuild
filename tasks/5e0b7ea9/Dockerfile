# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Make non-interactive
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    python3 -m pip install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------------------- #
# Prepare initial filesystem that the exercise relies on
# --------------------------------------------------------------------- #

# Create the user’s home if it doesn’t already exist
RUN mkdir -p /home/user

# Create application directory structure
RUN mkdir -p /home/user/webapp/config && \
    mkdir -p /home/user/webapp/tmp && \
    mkdir -p /home/user/webapp/logs

# Create baseline configuration file
RUN cat > /home/user/webapp/config/server.env <<'EOF'
APP_PORT=8080
LOG_LEVEL=info
DB_HOST=localhost
EOF

# Create baseline historical log file
RUN cat > /home/user/webapp/logs/webapp.log <<'EOF'
2023-10-09 12:34:56 [DEBUG] Connected to database
2023-10-09 12:35:01 [INFO]  Request processed
2023-10-09 12:35:02 [DEBUG] Cache miss for key: user_123
2023-10-09 12:35:04 [ERROR] Failed to send email
2023-10-09 12:35:05 [DEBUG] Retrying request id: 456
EOF

# Ensure everything is writable by the (non-root) user who will run tests
RUN chmod -R 777 /home/user/webapp

# Set permissions on home directory
RUN chmod 755 /home/user

# Metadata
LABEL Author="On-Call DevOps Exercise Generator" \
      Description="Environment for debug-logging configuration task with pytest pre-installed."