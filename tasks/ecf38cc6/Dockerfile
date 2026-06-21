FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create required directories
RUN mkdir -p /home/user/ci_artifacts && \
    mkdir -p /home/user/ci_cd_archives && \
    mkdir -p /home/user/task_output

# Populate build.log
RUN cat <<'EOF' > /home/user/ci_artifacts/build.log
BUILD START
Compiling modules...
All modules compiled.
BUILD END
Status: SUCCESS
EOF

# Populate test.log
RUN cat <<'EOF' > /home/user/ci_artifacts/test.log
TEST SUITE START
All 128 tests passed.
Duration: 00:01:34
TEST SUITE END
EOF

# Populate deploy.log
RUN cat <<'EOF' > /home/user/ci_artifacts/deploy.log
DEPLOYMENT START
Pushing container to registry...
Container SHA: abcdef123456
Scaling services...
DEPLOYMENT END
Status: SUCCESS
EOF

# Permissions
RUN chmod 777 /home/user && \
    chmod 777 /home/user/ci_artifacts && \
    chmod 777 /home/user/ci_cd_archives && \
    chmod 777 /home/user/task_output && \
    chmod 666 /home/user/ci_artifacts/*.log

# Environment variables (converted from %environment)
ENV PATH="$PATH:/usr/local/bin"

# Labels
LABEL Author="pipeline-setup"
LABEL Description="Container prepared for the 'pipeline logs backup' task. Contains initial log files and pytest preinstalled."

# Help text
# This container provides the starting point for the CI/CD pipeline log backup task.
# Log files are located in /home/user/ci_artifacts/, and pytest is installed for automated grading.