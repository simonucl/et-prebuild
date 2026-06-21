# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python, pip, setuptools, and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update -qq && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Provide a wrapper around the pytest entry-point that guarantees
# the required initial state exists every time pytest is invoked
# ------------------------------------------------------------------
RUN mv /usr/local/bin/pytest /usr/local/bin/pytest.real

RUN cat > /usr/local/bin/pytest << 'SH'
#!/bin/sh
# Wrapper to ensure the baseline file structure for the exercise is present
TARGET_DIR="/home/user/workspace/app/logs"
LOG_FILE="$TARGET_DIR/build_2023-09-01.log"

# Create directory tree if it does not yet exist
if [ ! -d "$TARGET_DIR" ]; then
    mkdir -p "$TARGET_DIR"
fi

# Create the baseline log file with the expected content if missing
if [ ! -f "$LOG_FILE" ]; then
    cat > "$LOG_FILE" <<'EOF'
2023-09-01 10:01:02 INFO [Init] Application started
2023-09-01 10:01:03 WARNING [Config] Missing optional setting "theme"
2023-09-01 10:01:04 ERROR [Database] Connection refused
2023-09-01 10:02:00 INFO [Heartbeat] Alive
2023-09-01 10:03:12 ERROR [Auth] Invalid credentials
2023-09-01 10:04:45 INFO [Shutdown] Application stopped
EOF
fi

# Hand off execution to the real pytest binary
exec /usr/local/bin/pytest.real "$@"
SH

RUN chmod +x /usr/local/bin/pytest

# ------------------------------------------------------------------
# Place the baseline file inside the image itself for completeness
# ------------------------------------------------------------------
RUN mkdir -p /home/user/workspace/app/logs

RUN cat > /home/user/workspace/app/logs/build_2023-09-01.log <<'EOF'
2023-09-01 10:01:02 INFO [Init] Application started
2023-09-01 10:01:03 WARNING [Config] Missing optional setting "theme"
2023-09-01 10:01:04 ERROR [Database] Connection refused
2023-09-01 10:02:00 INFO [Heartbeat] Alive
2023-09-01 10:03:12 ERROR [Auth] Invalid credentials
2023-09-01 10:04:45 INFO [Shutdown] Application stopped
EOF

RUN chmod -R a+rwX /home/user/workspace

# ------------------------------------------------------------------
# Environment setup (from %environment)
# ------------------------------------------------------------------
RUN mkdir -p /home/user && chmod 755 /home/user

# No environment variables are strictly necessary for the task.