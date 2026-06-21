# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels converted from %labels
LABEL Author="ChatGPT"
LABEL Description="Environment for cluster provisioning log summarisation task"

# ---------------------------------------------------------------------
# 1. Basic tools and Python (needed for pytest which the checker uses)
# ---------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        gnupg \
        curl && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------
# 2. Create the expected filesystem structure and log file
# ---------------------------------------------------------------------
RUN mkdir -p /home/user/logs

RUN cat <<'EOF' > /home/user/logs/provisioning.log
2023-10-22T08:00:01Z INFO Provisioning started: server id=db-001
2023-10-22T08:00:40Z ERROR Provisioning failed: server id=db-001 reason=timeout
2023-10-22T09:15:11Z INFO Provisioning started: server id=web-101
2023-10-22T09:16:03Z INFO Provisioning succeeded: server id=web-101
2023-10-22T10:22:45Z INFO Provisioning started: server id=cache-007
2023-10-22T10:23:20Z INFO Provisioning succeeded: server id=cache-007
2023-10-22T11:01:00Z INFO Provisioning started: server id=api-055
2023-10-22T11:02:47Z ERROR Provisioning failed: server id=api-055 reason=credentials
2023-10-22T12:30:05Z INFO Provisioning started: server id=worker-230
2023-10-22T12:31:39Z INFO Provisioning succeeded: server id=worker-230
EOF

# ---------------------------------------------------------------------
# 3. Ensure non-root users can read the log and its directories
# ---------------------------------------------------------------------
RUN chmod -R 755 /home/user

# ---------------------------------------------------------------------
# Environment variables from %environment
# ---------------------------------------------------------------------
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# ---------------------------------------------------------------------
# Default run behavior converted from %runscript
# ---------------------------------------------------------------------
CMD echo "This container is configured for the provisioning summary task." && \
    echo "Execute your own commands or tests as needed."