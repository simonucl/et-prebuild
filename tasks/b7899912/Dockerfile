# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text from %help
# This container provides the initial state for a monitoring-alert assignment.
# It already contains:
#   • /home/user/data/metrics.csv with predefined rows.
#   • Python 3 and pytest for running the verification suite.
#   • jq (and standard coreutils) in case the student prefers CLI tools.
# Students are expected to generate /home/user/alerts/high_usage.json
# and /home/user/alerts/process.log according to the task description.

LABEL Author="Auto-generated definition for monitoring alert task"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data

RUN cat <<'EOF' > /home/user/data/metrics.csv
server,cpu,memory
web-01,65,70
app-02,88,91
db-01,92,80
cache-01,55,40
web-02,83,95
EOF

RUN chmod 0777 /home/user