# Converted from Apptainer definition
FROM ubuntu:22.04

# Install Python3, pip, pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create initial filesystem state
RUN mkdir -p /home/user/logs

RUN cat >/home/user/logs/app.log <<'EOF'
2023-07-21 10:33:45,123 [INFO] [user-service] User 'alice' logged in from 10.0.0.12 (session:abc123)
2023-07-21 11:12:07,456 [INFO] [user-service] User 'bob' logged in from 10.0.0.15 (session:def456)
2023-07-21 12:55:22,789 [INFO] [user-service] User 'charlie' logged in from 10.0.0.18 (session:ghi789)
EOF

RUN chmod 0777 /home/user/logs

# Environment setup
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

RUN chmod 755 /home/user

# Labels
LABEL Author="DevOps-Challenge-Prep"
LABEL Description="Container for login audit log parsing task"

# Help text (as comments)
# This image provides the initial state and dependencies
# for the login audit log parsing exercise.
# A raw log is placed in /home/user/logs/app.log.
# Participants must generate /home/user/logs/login_summary.log.
# Pytest is installed so the automated grader can verify results.