# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer %labels
LABEL Author="ChatGPT" \
      Description="Container for log-filtering exercise; provides initial state and pytest."

# Updating package index and installing Python tooling
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Installing pytest
RUN --mount=type=cache,target=/root/.cache/pip set -e && \
    pip3 install --no-cache-dir pytest

# Creating user 'user' and project directory structure
RUN set -e && \
    if ! id -u user >/dev/null 2>&1; then \
        useradd -m -s /bin/bash user; \
    fi && \
    PROJECT_DIR=/home/user/project && \
    mkdir -p "${PROJECT_DIR}"

# Populating initial log file
RUN cat > "/home/user/project/app.log" <<'EOF'
2024-01-01 10:00:00 INFO  [INIT] - Application started
2024-01-01 10:00:01 WARN  [CONFIG] - Missing optional field 'foo'
2024-01-01 10:00:02 ERROR [AUTH] - ERR42 - Authentication failed for user 'alice'
2024-01-01 10:00:03 ERROR [DB] - ERR13 - Database connection lost
2024-01-01 10:00:04 INFO  [AUTH] - User 'alice' retry
2024-01-01 10:00:05 ERROR [AUTH] - ERR42 - Authentication failed for user 'alice'
2024-01-01 10:00:06 ERROR [AUTH] - ERR42 - Authentication failed for user 'bob'
2024-01-01 10:00:07 WARN  [NET] - Network latency above threshold
2024-01-01 10:00:08 ERROR [DB] - ERR13 - Database connection lost
2024-01-01 10:00:09 ERROR [AUTH] - ERR99 - Token expired for user 'carol'
2024-01-01 10:00:10 INFO  [SHUTDOWN] - Application stopped
EOF

# Setting permissions and ensuring artefact files do NOT exist yet
RUN set -e && \
    chmod 644 "/home/user/project/app.log" && \
    chmod 755 /home/user "/home/user/project" && \
    rm -f "/home/user/project/error_lines.log" "/home/user/project/error_summary.txt"

# %help
# This image supplies:
#   • /home/user/project/app.log   (initial log file)
#   • pytest                       (installed via pip)
#
# The exercise agent must create:
#   • /home/user/project/error_lines.log
#   • /home/user/project/error_summary.txt