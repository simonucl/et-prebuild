FROM ubuntu:22.04

# Labels
LABEL Author="CloudMigrationSetup"
LABEL Description="Environment for cloud-migration task with proper initial state and pytest installed."

# Post installation
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    mkdir -p /home/user/legacy_service && \
    chmod 700 /home/user/legacy_service

# Create config.ini with EXACT required contents (4 lines)
RUN cat > /home/user/legacy_service/config.ini <<'EOF'
[server]
host = 127.0.0.1
port = 5000

EOF

# Create writable migration.log (leave empty)
RUN touch /home/user/migration.log && \
    chmod 666 /home/user/migration.log

# Create the singularity environment hook directory and script for compatibility
RUN mkdir -p /.singularity.d/env

RUN cat > /.singularity.d/env/99-fix-perms.sh <<'EOSH'
#!/bin/sh
# Make sure the current user owns the critical paths so that 0700 works.
# Suppress errors if chown/chmod fail (e.g., already owned).
chown "$(id -u)":"$(id -g)" /home/user/legacy_service 2>/dev/null || true
chown "$(id -u)":"$(id -g)" /home/user/migration.log 2>/dev/null || true
chmod 700 /home/user/legacy_service 2>/dev/null || true
EOSH

RUN chmod 755 /.singularity.d/env/99-fix-perms.sh

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:$PATH"

# Set working directory
WORKDIR /home/user

# Default command: open an interactive shell
CMD ["/bin/bash"]

# Help information (as comments):
# This container sets up the initial state for the "cloud-migration"
# exercise and includes pytest for the automated grader.