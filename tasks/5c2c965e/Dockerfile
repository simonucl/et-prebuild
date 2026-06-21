# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Apptainer Task Generator" \
      Description="Container for log-processing one-liner exercise"

# ------------------------------------------------------------------
# Install system dependencies, Python, pip, and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Create directory structure and initial log file
# ------------------------------------------------------------------
RUN mkdir -p /home/user/projects/myapp/logs

RUN cat <<'EOF' >/home/user/projects/myapp/logs/app.log
2024-05-30 12:00:01,001 INFO  Starting application
2024-05-30 12:00:02,002 ERROR Failed to connect to database
2024-05-30 12:00:03,003 WARN  Cache miss for key user_123
2024-05-30 12:00:04,004 ERROR Null pointer exception in module XYZ
2024-05-30 12:00:05,005 INFO  Processing request id=987
2024-05-30 12:00:06,006 ERROR Timeout while contacting external API
2024-05-30 12:00:07,007 DEBUG Retrying connection
2024-05-30 12:00:08,008 ERROR Invalid credentials for user 'admin'
2024-05-30 12:00:09,009 INFO  Shutdown sequence initiated
2024-05-30 12:00:10,010 ERROR Unhandled exception in main loop
EOF

# ------------------------------------------------------------------
# Ensure proper permissions
# ------------------------------------------------------------------
RUN chmod 755 /home/user && \
    chmod -R 755 /home/user/projects && \
    chmod 644 /home/user/projects/myapp/logs/app.log

# ------------------------------------------------------------------
# Environment variables from Apptainer %environment
# ------------------------------------------------------------------
ENV PATH="/usr/local/bin:${PATH}" \
    LC_ALL="C.UTF-8" \
    LANG="C.UTF-8"