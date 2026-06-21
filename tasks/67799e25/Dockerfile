# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Apptainer setup for error-report exercise" \
      Description="Container pre-provisioned with log files and pytest for automated grading."

# Set environment variables
ENV LC_ALL=C \
    LANG=C

# Update APT metadata and install Python + Pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state for the “error-report” exercise
RUN set -e && \
    mkdir -p /home/user/logs && \
    chmod 755 /home/user && \
    chmod 755 /home/user/logs

# Create the deployment log with exact contents
RUN cat > /home/user/logs/release-2023-07-01.log << 'EOF'
2023-07-01 10:15:02 [INFO] Starting deployment
2023-07-01 10:15:05 [WARN] Slow response from artifact repository
2023-07-01 10:15:10 [ERROR] Failed to fetch artifact build-1234
2023-07-01 10:15:12 [INFO] Retrying...
2023-07-01 10:15:18 [ERROR] Failed to fetch artifact build-1234
2023-07-01 10:15:30 [INFO] Deployment aborted
2023-07-01 10:15:31 [ERROR] Rollback failed: missing snapshot
2023-07-01 10:15:35 [INFO] Manual intervention required
EOF

RUN chmod 644 /home/user/logs/release-2023-07-01.log

# %runscript equivalent (no default action)
# Container for the error-report task (no default action).