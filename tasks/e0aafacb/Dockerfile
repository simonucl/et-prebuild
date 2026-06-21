FROM ubuntu:22.04

# Author incident-response-template
# This container provides the initial filesystem state for the alert-processing
# exercise.  It includes:
#   • /home/user/data/alerts.csv  — CSV source data
#   • /home/user/output/          — empty writable directory for results
#
# Pytest is pre-installed for automated grading.

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the required user directory structure
RUN mkdir -p /home/user/data && \
    mkdir -p /home/user/output

# Populate alerts.csv with the exact required contents (including final newline)
RUN cat > /home/user/data/alerts.csv <<'EOF'
id,timestamp,severity,description
A1,2024-07-15T11:22:33Z,high,CPU usage >90%
A2,2024-07-15T11:25:10Z,medium,Disk read latency
A3,2024-07-15T11:30:22Z,high,Unauthorised login attempt
A4,2024-07-15T11:35:42Z,low,Service restart completed
EOF

# Ensure correct permissions (readable by all, writable by the running user layer)
RUN chmod 755 /home/user && \
    chmod 755 /home/user/data /home/user/output && \
    chmod 644 /home/user/data/alerts.csv

WORKDIR /home/user