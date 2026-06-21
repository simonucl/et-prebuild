# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="example@sre.local" \
      Description="Container preloaded with uptime sample data and pytest for SRE incident-readiness exercise."

# ------------------------------------------------------------------
# Post section: install packages and prepare filesystem
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test harness
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create the user’s home data directory
RUN mkdir -p /home/user/data

# Write the canonical uptime sample CSV (LF endings, final newline)
RUN cat > /home/user/data/uptime_sample.csv <<'CSVEND'
timestamp,service,status
2023-09-01T00:00:00Z,auth-service,UP
2023-09-01T00:01:00Z,auth-service,DOWN
2023-09-01T00:02:00Z,auth-service,UP
2023-09-01T00:00:00Z,api-gateway,UP
2023-09-01T00:01:00Z,api-gateway,UP
2023-09-01T00:02:00Z,api-gateway,DOWN
2023-09-01T00:03:00Z,api-gateway,DOWN
2023-09-01T00:04:00Z,api-gateway,UP
CSVEND

# Ensure appropriate permissions (read/write for container user UID)
RUN chmod 644 /home/user/data/uptime_sample.csv

# ------------------------------------------------------------------
# Environment section
# ------------------------------------------------------------------

# Ensure home directory has appropriate permissions
RUN chmod 755 /home/user

# Make sure Python is easily accessible
ENV PATH=/usr/bin:$PATH

# ------------------------------------------------------------------
# Help:
# Container preloaded with uptime sample data and pytest for
# SRE incident-readiness exercise.
# ------------------------------------------------------------------