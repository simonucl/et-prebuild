FROM ubuntu:22.04

# Labels
LABEL Author="MyApp Task Preparer"
LABEL Description="Environment preset for \"myapp\" configuration report task."

# Help section as comments:
# This Docker image provides the initial state for the "myapp" audit-log
# parsing exercise.  It includes:
#   • /home/user/config_audit.log   – the source audit log
#   • pytest                        – for automated grading tests

# Update package list and install Python + pip
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates

# Install pytest for the test-runner that will be executed later
RUN python3 -m pip install --no-cache-dir --upgrade pip pytest

# Prepare initial task state
# Ensure /home/user exists and is writable by whoever runs the container
RUN mkdir -p /home/user && \
    chmod 1777 /home/user

# Create the predefined audit log with the exact required contents
RUN cat >/home/user/config_audit.log <<'EOF'
2023-07-01 12:00:00 | myapp.conf | ADDED   | enable_feature=true
2023-07-01 12:05:00 | myapp.conf | CHANGED | max_connections 100->150
2023-07-02 08:00:00 | myapp.conf | CHANGED | timeout 30->45
2023-07-03 09:30:00 | myapp.conf | REMOVED | debug_mode
EOF

# Set file permissions to rw-r--r-- (644)
RUN chmod 644 /home/user/config_audit.log

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Set working directory
WORKDIR /home/user