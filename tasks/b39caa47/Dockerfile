# syntax=docker/dockerfile:1
# Converted from Apptainer definition file
FROM ubuntu:22.04

# Post section
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    echo "Updating package index and installing Python tooling..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    echo "Installing pytest..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating directory structure for the exercise..." && \
    mkdir -p /home/user/logs

RUN echo "Populating /home/user/logs/failed_logins.csv with canonical content..." && \
    cat > /home/user/logs/failed_logins.csv << 'EOF'
user,timestamp,ip,reason
alice,2023-08-21T12:05:34Z,192.168.1.45,invalid_password
bob,2023-08-21T12:06:02Z,192.168.1.45,invalid_password
carol,2023-08-21T12:10:11Z,10.0.0.3,account_locked
dan,2023-08-21T12:11:47Z,10.0.0.3,invalid_password
erin,2023-08-21T12:12:33Z,192.168.1.100,invalid_password
frank,2023-08-21T12:13:01Z,10.0.0.3,invalid_password
EOF

RUN chmod 0777 /home/user && \
    chmod 0755 /home/user/logs && \
    chmod 0644 /home/user/logs/failed_logins.csv

# Environment section
ENV PATH="/usr/bin:${PATH}"

# Help text
# This container provides the initial filesystem state and required
# dependencies (Python 3 and pytest) for the "failed authentication"
# on-call incident response exercise.

# Labels
LABEL Author="oncall-failed-auth-task"
LABEL Description="Container for the failed authentication investigation exercise"