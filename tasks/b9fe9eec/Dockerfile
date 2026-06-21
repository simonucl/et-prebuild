# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text
# This Apptainer image provides the initial state for the “log-directory backup
# dry-run” task. Only /home/user/app/logs/app.log is pre-populated; no backup
# or monitoring artefacts are present. Pytest is installed for automated
# evaluation.

LABEL Maintainer="AI_Apptainer_Setup"
LABEL Description="Environment for backup dry-run task – contains initial log directory only."

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /home/user/app/logs

RUN cat > /home/user/app/logs/app.log <<'EOF'
2024-01-05 12:00:00 Application started
2024-01-05 12:05:00 Application running
EOF

RUN chmod 1777 /home/user