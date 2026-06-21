FROM ubuntu:22.04

# Labels
LABEL Author="SecurityAudit Task Setup"
LABEL Description="Initial state for audit_demo permissions task."

# Update package lists and install Python + pip
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        git \
        curl && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create the directory structure
RUN mkdir -p /home/user/audit_demo

# Create the credentials file using heredoc
RUN cat >/home/user/audit_demo/credentials.txt <<'EOF'
username=admin
password=Passw0rd!
token=SECRETTOKEN123
EOF

# Set initial permissions as described in the task
RUN chmod 755 /home/user/audit_demo && \
    chmod 644 /home/user/audit_demo/credentials.txt && \
    chown -R 0:0 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Help information as comments
# This container provides the starting environment for the
# "Audit Demo Permissions" task.  It contains:
#
#   /home/user/audit_demo                  (mode 755)
#   /home/user/audit_demo/credentials.txt  (mode 644)
#
# Pytest is pre-installed so the automated grader can run its tests.