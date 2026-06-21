# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Container image that sets up the initial filesystem state for the
# “distributed time-out analysis” programming exercise.
# ------------------------------------------------------------------

LABEL Author="Time-out-Exercise-Builder"

# ------------------------------------------------------------------
# 1. Base tooling: make sure Python and pytest are available
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# 2. Prepare initial workspace expected by the exercise
# ------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/distributed_logs

# ----- serviceA.log ------------------------------------------------
RUN cat > /home/user/distributed_logs/serviceA.log << 'EOF'
2023-10-18T02:12:00Z SERVICE_A INFO  Node=alpha   Msg="Heartbeat"
2023-10-18T02:13:45Z SERVICE_A ERROR Node=alpha   Msg="Timeout while contacting Node beta"
2023-10-18T02:14:30Z SERVICE_A INFO  Node=alpha   Msg="Recovered connection"
2023-10-18T02:15:01Z SERVICE_A ERROR Node=alpha   Msg="Timeout while contacting Node gamma"
2023-10-18T02:16:30Z SERVICE_A WARN  Node=alpha   Msg="High latency detected"
2023-10-17T23:59:59Z SERVICE_A ERROR Node=alpha   Msg="Timeout while contacting Node delta"
EOF

# ----- serviceB.log ------------------------------------------------
RUN cat > /home/user/distributed_logs/serviceB.log << 'EOF'
2023-10-18T02:13:00Z SERVICE_B INFO  Node=bravo   Msg="Heartbeat"
2023-10-18T02:14:00Z SERVICE_B ERROR Node=bravo   Msg="Timeout while contacting Node delta"
2023-10-18T02:15:30Z SERVICE_B INFO  Node=bravo   Msg="Recovered connection"
2023-10-18T02:16:17Z SERVICE_B ERROR Node=bravo   Msg="Timeout while contacting Node epsilon"
EOF

# ----- serviceC.log ------------------------------------------------
RUN cat > /home/user/distributed_logs/serviceC.log << 'EOF'
2023-10-18T02:14:30Z SERVICE_C ERROR Node=charlie Msg="Timeout while contacting Node alpha"
EOF

# Ensure the files are world-readable and home directory has proper permissions
RUN chmod 644 /home/user/distributed_logs/*.log && \
    chmod 755 /home/user