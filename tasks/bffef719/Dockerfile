# syntax=docker/dockerfile:1
# Converted from Apptainer definition file
FROM ubuntu:22.04

# Update apt cache and install Python & pip
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create directories and set permissions
RUN mkdir -p /home/user/build_logs && \
    chmod 0777 /home/user/build_logs

# Populate the CI build log
RUN cat > /home/user/build_logs/ci_build.log <<'EOF'
[2023-09-12 10:15:01] [INFO] Starting build step 1
[2023-09-12 10:15:05] [ERROR] Failed to fetch dependencies
[2023-09-12 10:16:12] [WARN] Deprecated API usage
[2023-09-12 10:17:30] [INFO] Running unit tests
[2023-09-12 10:17:45] [ERROR] Unit test failures detected
[2023-09-12 10:18:02] [INFO] Build completed
[2023-09-12 10:18:06] [ERROR] Post-build hook failed
EOF

RUN chmod 0644 /home/user/build_logs/ci_build.log

# Ensure home directory permissions
RUN chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:$PATH"

# Labels
LABEL Author="Apptainer Task Setup"
LABEL Description="Container with initial CI build log and pytest installed for agent task."

# Help text
# This Apptainer image sets up the environment for the CI build log
# filtering task, providing:
#   • /home/user/build_logs/ci_build.log with predefined contents
#   • Writable /home/user/build_logs directory for the agent
#   • Python 3 and pytest pre-installed