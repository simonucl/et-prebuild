# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------
# Install system dependencies, Python, pip, and pytest
# ------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Prepare initial filesystem state for the grading task
# ------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user/builds && \
    chmod 0755 /home/user && \
    chmod 0777 /home/user/builds

# Create the pre-existing log file with specific contents
RUN cat > /home/user/builds/jenkins_build.log <<'EOF'
[2023-09-01 12:00:00] Starting build
[2023-09-01 12:05:00] BUILD SUCCESS
[2023-09-02 14:10:17] Starting build
[2023-09-02 14:15:30] BUILD FAILURE
[2023-09-03 09:00:00] Starting build
[2023-09-03 09:07:42] BUILD SUCCESS
[2023-09-04 11:22:10] Starting build
[2023-09-04 11:29:58] BUILD SUCCESS
EOF

# Ensure correct permissions on the log file
RUN chmod 0644 /home/user/builds/jenkins_build.log

# ------------------------------------------------------------
# Runtime environment variables
# ------------------------------------------------------------
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# ------------------------------------------------------------
# Labels
# ------------------------------------------------------------
LABEL Author="build-eng-prep" \
      Description="Container prepared for CI log-analysis shell task with pytest pre-installed"