FROM ubuntu:22.04

# Labels
LABEL Author="CloudMigrationPrep"
LABEL Description="Environment for rsync-synchronisation assignment"

# Install required system packages
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        rsync \
        ca-certificates \
        tzdata && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Create an unprivileged user that will own the working files
# UID/GID 1000 is the conventional first user on Linux systems.
RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user

# Prepare the initial directory hierarchy expected by the tests
RUN install -o 1000 -g 1000 -d /home/user/project_data && \
    install -o 1000 -g 1000 -d /home/user/remote_backup && \
    install -o 1000 -g 1000 -d /home/user/sync_logs

# Create data1.txt
RUN cat > /home/user/project_data/data1.txt <<'EOF'
Alpha
Beta
Gamma
EOF

# Create data2.cfg
RUN cat > /home/user/project_data/data2.cfg <<'EOF'
[settings]
mode=production
EOF

# Create data3.json
RUN cat > /home/user/project_data/data3.json <<'EOF'
{
  "version": 1.2,
  "enabled": true
}
EOF

# Ensure correct ownership for the three source files
RUN chown 1000:1000 /home/user/project_data/data1.txt \
                    /home/user/project_data/data2.cfg \
                    /home/user/project_data/data3.json

# Populate /home/user/remote_backup with a single stale file
RUN echo 'OldData' > /home/user/remote_backup/data1.txt && \
    chown 1000:1000 /home/user/remote_backup/data1.txt

# Permissions: make sure everything is writable by the non-root user
RUN chmod -R u+rwX,go+rX /home/user

# Environment variables
ENV PATH="$PATH:/home/user/.local/bin"

# Default command
CMD echo "Container for rsync synchronisation assignment." && \
    echo "Switch to the 'user' account and complete the exercise as described."