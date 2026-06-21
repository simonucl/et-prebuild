# Converted from Apptainer definition file
FROM ubuntu:22.04

# Install Python, pip, pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directory structure
RUN mkdir -p /home/user/provisioning/scripts/utils

# deploy.sh
RUN cat <<'EOF' > /home/user/provisioning/scripts/deploy.sh
#!/bin/bash
echo "Deploying application..."
EOF

# teardown.sh
RUN cat <<'EOF' > /home/user/provisioning/scripts/teardown.sh
#!/bin/bash
echo "Tearing down..."
EOF

# utils/common.sh
RUN cat <<'EOF' > /home/user/provisioning/scripts/utils/common.sh
#!/bin/bash
log() { echo "[`date`] $1"; }
EOF

# README.md
RUN cat <<'EOF' > /home/user/provisioning/scripts/README.md
# Provisioning Scripts
This directory contains helper scripts for deploying and tearing down infrastructure.
EOF

# Permissions
RUN chmod 755 /home/user/provisioning/scripts/deploy.sh && \
    chmod 755 /home/user/provisioning/scripts/teardown.sh && \
    chmod 755 /home/user/provisioning/scripts/utils/common.sh && \
    chmod 644 /home/user/provisioning/scripts/README.md && \
    chmod -R a+rX /home/user

# Environment variables
ENV PATH="$PATH:/usr/local/bin"

# Run script
CMD echo "Container for provisioning-scripts backup task. Execute your solution script inside this container."