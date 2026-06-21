# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="DeploymentPrep" \
      Description="Container with initial log state for deployment-report task."

# ----------------------------
# Post section
# ----------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create directory tree
RUN mkdir -p /home/user/deployment/logs

# Populate log files
RUN cat > /home/user/deployment/logs/2023-09-01.log <<'EOF'
2023-09-01 02:15:12 [web-01] STATUS: OK
2023-09-01 02:16:05 [db-01] STATUS: FAIL
2023-09-01 02:17:45 [cache-01] STATUS: OK
2023-09-01 02:18:20 [auth-01] STATUS: FAIL
EOF

RUN cat > /home/user/deployment/logs/2023-09-02.log <<'EOF'
2023-09-02 02:14:02 [web-02] STATUS: OK
2023-09-02 02:15:47 [db-02] STATUS: OK
2023-09-02 02:16:37 [cache-02] STATUS: OK
2023-09-02 02:18:55 [auth-02] STATUS: OK
EOF

RUN cat > /home/user/deployment/logs/2023-09-03.log <<'EOF'
2023-09-03 02:13:33 [web-03] STATUS: OK
2023-09-03 02:15:02 [db-03] STATUS: FAIL
2023-09-03 02:16:58 [cache-03] STATUS: FAIL
2023-09-03 02:17:42 [auth-03] STATUS: OK
EOF

# Set permissions
RUN chmod 0777 /home/user /home/user/deployment && \
    chmod 0755 /home/user/deployment/logs && \
    chmod 0644 /home/user/deployment/logs/*.log

# ----------------------------
# Environment section
# ----------------------------
# No environment variables to override; rely on default HOME binding.

# ----------------------------
# Help section
# ----------------------------
# This image provides the exact initial filesystem state required for
# the deployment-report exercise.
# It contains:
#  • Python 3 and pytest (available system-wide).
#  • The directory /home/user/deployment/logs/ with the three raw log files.
# No report directories or files have been created.