FROM ubuntu:22.04

# Labels
LABEL Author="restore-task-image"
LABEL Description="Environment for static website restore exercise with pytest pre-installed."

# Post installation commands
RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        iproute2 \
        lsof \
        ca-certificates \
        tar && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test-harness
RUN pip3 install --no-cache-dir pytest

# Create backup directory structure
RUN mkdir -p /home/user/backup

# Create the exact HTML file expected in the tarball
RUN cat > /tmp/index.html <<'EOF'
<html>
<body>
<h1>Backup Restore Successful</h1>
</body>
</html>
EOF

# Package it into site_backup.tar.gz with path "index.html"
RUN tar -czf /home/user/backup/site_backup.tar.gz -C /tmp index.html

# Remove temporary working file
RUN rm /tmp/index.html

# Ensure write permissions for the runtime (non-root) user
RUN chmod 1777 /home/user && \
    chmod -R a+rX /home/user/backup && \
    chmod -R a+rw /home/user/backup

# Environment variables
ENV PATH=$PATH

# Set working directory
WORKDIR /home/user