# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer %labels
LABEL Author="devops-task-generator" \
      Description="Initial state for “Batch-handling log files with find + xargs” exercise"

# ------------------------------------------------------------------
# Install Python and pytest for the testing framework
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Create initial directory structure and log files for the exercise
# ------------------------------------------------------------------
RUN mkdir -p /home/user/logs/app1 && \
    mkdir -p /home/user/logs/app2

# ------------------------------------------------------------------
# Populate app1 log files
# ------------------------------------------------------------------
RUN cat > /home/user/logs/app1/app1-2023-09-01.log <<'EOF'
[2023-09-01 12:00:00] INFO  Application started
[2023-09-01 12:05:10] ERROR (E101) Failed to connect to DB
[2023-09-01 12:06:00] INFO  Application stopped
EOF

RUN cat > /home/user/logs/app1/app1-2023-09-15.log <<'EOF'
[2023-09-15 09:00:00] INFO  Application started
[2023-09-15 09:15:27] ERROR (E202) Timeout while processing
[2023-09-15 10:00:00] ERROR (E101) Failed to connect to DB
[2023-09-15 11:00:00] INFO  Application stopped
EOF

# ------------------------------------------------------------------
# Populate app2 log files
# ------------------------------------------------------------------
RUN cat > /home/user/logs/app2/app2-2023-09-10.log <<'EOF'
[2023-09-10 08:00:00] INFO  Start
[2023-09-10 08:05:00] ERROR (E303) Disk full
[2023-09-10 08:06:00] INFO  End
EOF

RUN cat > /home/user/logs/app2/app2-2023-09-18.log <<'EOF'
[2023-09-18 07:00:00] INFO  Start
[2023-09-18 07:30:00] ERROR (E202) Timeout while processing
[2023-09-18 08:00:00] INFO  End
EOF

# ------------------------------------------------------------------
# Set permissions: ensure directories are user-writable and files readable
# ------------------------------------------------------------------
RUN chmod -R 0777 /home/user

# ------------------------------------------------------------------
# Environment variables from Apptainer %environment
# ------------------------------------------------------------------
ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Note: The /home/user/archive directory and any derived artefacts
# MUST NOT exist at build time; they will be created during the exercise.

# ------------------------------------------------------------------
# Help text from Apptainer %help
# ------------------------------------------------------------------
# This container provides the starting filesystem state for the
# “Batch-handling log files with find + xargs” task.