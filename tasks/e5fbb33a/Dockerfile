FROM ubuntu:22.04

# Labels
LABEL Maintainer="rotation-task-setup"
LABEL Description="Initial state for credential-rotation exercise"

# Install Python tooling and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial directory structure and files
# Create the pipeline directories
RUN mkdir -p /home/user/data_pipeline/config

# Make sure they are writable by any unprivileged user that will run
# inside the container.
RUN chmod -R a+rwx /home && \
    chmod -R a+rwx /home/user

# Create the initial credentials.env file with the exact
# three-line content required by the task specification.
RUN cat > /home/user/data_pipeline/config/credentials.env <<'EOF'
DB_USER=analytics_user
DB_PASSWORD=oldPass123
API_KEY=oldApiKey456
EOF

# Ensure the file is readable (and modifiable) by non-root users.
RUN chmod 644 /home/user/data_pipeline/config/credentials.env

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8