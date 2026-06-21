FROM ubuntu:22.04

# Labels
LABEL Author="backup-task-builder"
LABEL Description="Initial state for backup automation task – includes pytest and predefined data/backup directories."

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the user home hierarchy
RUN mkdir -p /home/user/data && \
    mkdir -p /home/user/backup

# Populate /home/user/data with the expected files
RUN cat > /home/user/data/report.txt <<'EOF'
Quarterly report Q3 2023
EOF

RUN cat > /home/user/data/config.cfg <<'EOF'
max_connections=100
EOF

# Ensure correct permissions
RUN chmod 0755 /home/user && \
    chmod 0755 /home/user/data && \
    chmod 0777 /home/user/backup && \
    chmod 0644 /home/user/data/report.txt /home/user/data/config.cfg

# Environment variables
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin