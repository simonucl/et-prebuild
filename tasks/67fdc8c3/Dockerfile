# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Daily-Summary Exercise Container" \
      Description="Starting filesystem state for the daily summary task. Pytest pre-installed."

# Base system setup and Python installation
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install pytest
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial log files and directory structure
RUN mkdir -p /home/user/logs

# Create the automation_events.log with exact contents
RUN cat > /home/user/logs/automation_events.log <<'EOF'
2024-04-12 08:00:01 INFO TaskScheduler: TASK_START id=120 type=cleanup
2024-04-12 08:00:03 INFO TaskProcessor: TASK_SUCCESS id=120 duration=2s
2024-04-12 09:15:00 INFO TaskScheduler: TASK_START id=121 type=backup
2024-04-12 09:15:20 ERROR TaskProcessor: TASK_FAIL id=121 reason=NO_SPACE
2024-04-12 09:45:10 INFO TaskScheduler: TASK_START id=122 type=deploy
2024-04-12 09:45:45 INFO TaskProcessor: TASK_SUCCESS id=122 duration=35s
2024-04-12 10:05:11 INFO TaskScheduler: TASK_START id=123 type=backup
2024-04-12 10:05:40 ERROR TaskProcessor: TASK_FAIL id=123 reason=TIMEOUT
2024-04-12 11:30:04 INFO TaskScheduler: TASK_START id=124 type=cleanup
2024-04-12 11:30:05 ERROR TaskProcessor: TASK_FAIL id=124 reason=PERMISSION_DENIED
2024-04-12 12:00:22 INFO TaskScheduler: TASK_START id=125 type=backup
2024-04-12 12:00:52 INFO TaskProcessor: TASK_SUCCESS id=125 duration=30s
2024-04-12 13:20:30 INFO TaskScheduler: TASK_START id=126 type=deploy
2024-04-12 13:21:10 INFO TaskProcessor: TASK_SUCCESS id=126 duration=40s
2024-04-12 14:44:55 INFO TaskScheduler: TASK_START id=127 type=cleanup
2024-04-12 14:45:01 ERROR TaskProcessor: TASK_FAIL id=127 reason=NO_SPACE
EOF

# Ensure correct permissions
RUN chmod 755 /home/user && \
    chmod 755 /home/user/logs && \
    chmod 644 /home/user/logs/automation_events.log