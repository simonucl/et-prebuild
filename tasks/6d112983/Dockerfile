# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# -------------------------- #
# Install Python & pytest    #
# -------------------------- #
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# -------------------------- #
# Prepare initial filesystem #
# -------------------------- #
# Create the /home/user directory tree expected by the exercise
RUN set -e && \
    mkdir -p /home/user/logs && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/logs

# Create the production log file with the exact required content
RUN cat > /home/user/logs/server.log <<'EOF'
2023-11-25 10:01:02 INFO User logged in
2023-11-25 10:02:15 ERROR 500 Internal Server Error at /login
2023-11-25 10:03:47 WARN Disk space low
2023-11-25 10:04:01 ERROR 404 Page Not Found /favicon.ico
2023-11-25 10:05:19 ERROR 500 Internal Server Error at /api/data
2023-11-25 10:06:33 ERROR 503 Service Unavailable at /reports
2023-11-25 10:07:45 INFO Job completed
2023-11-25 10:08:59 ERROR 500 Internal Server Error at /dashboard
2023-11-25 10:09:14 ERROR 503 Service Unavailable at /login
2023-11-25 10:10:21 ERROR 404 Page Not Found /robots.txt
2023-11-25 10:12:30 ERROR 502 Bad Gateway at /metrics
EOF

# Ensure permissions match the specification
RUN chmod 0644 /home/user/logs/server.log

# Metadata labels
LABEL Author="devops-task-generator" \
      Description="Container for log analysis task. Includes pytest and pre-populated server.log."

# -------------------------- #
# Help / Documentation       #
# -------------------------- #
# This image provides the starting environment for the log-analysis task.
# It contains:
#   • Python 3 and pytest for automated grading
#   • /home/user/logs/server.log with predefined content and correct permissions