# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Release Engineering Prep Container"
LABEL Description="Sets up initial state for deployment-frequency reporting task with pytest installed."

# Update apt and install Python, pip, and dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    echo "Updating apt and installing Python & pip..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest via pip
RUN --mount=type=cache,target=/root/.cache/pip echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir pytest

# Create directory structure and set permissions
RUN echo "Creating initial directory structure under /home/user..." && \
    mkdir -p /home/user/releases && \
    echo "Setting directory permissions to be writable by any user..." && \
    chmod 0777 /home/user/releases

# Populate deployment history log with exact contents
RUN echo "Populating deployment_history_2023-08.log with exact contents..." && \
    cat > /home/user/releases/deployment_history_2023-08.log <<'EOF'
2023-08-01 04:15:22 myservice:1.4.0
2023-08-01 05:00:41 auth:2.3.1
2023-08-02 06:32:10 myservice:1.4.0
2023-08-02 07:01:11 payments:3.1.0
2023-08-03 08:15:22 myservice:1.4.2
2023-08-03 09:36:15 auth:2.3.1
2023-08-04 10:44:55 payments:3.1.0
2023-08-04 11:22:33 payments:3.1.0
2023-08-05 12:30:45 myservice:1.4.2
2023-08-05 13:11:09 auth:2.3.2
EOF

# Ensure correct file permissions for the log file
RUN chmod 0644 /home/user/releases/deployment_history_2023-08.log && \
    echo "Initial state prepared."

# Ensure home directory permissions
RUN chmod 755 /home/user

# Environment variables from Apptainer %environment
ENV PYTHONIOENCODING=UTF-8
ENV LC_ALL=C.UTF-8