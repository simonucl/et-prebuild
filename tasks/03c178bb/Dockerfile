FROM ubuntu:22.04

# Update package lists and install Python + pip
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        build-essential

# Install pytest for the verification suite
RUN pip3 install --no-cache-dir pytest

# -----------------------------------------------------------------------------
# Prepare initial filesystem state expected by the grading tests
# -----------------------------------------------------------------------------

# Create required directory hierarchy
RUN mkdir -p /home/user/deploy/app && \
    mkdir -p /home/user/deploy/backups

# Populate live application directory with the two specified files
RUN echo "Hello World v1" > /home/user/deploy/app/index.html && \
    printf "version: 1.0\n" > /home/user/deploy/app/config.yaml

# Ensure the backups directory is empty (should already be)
RUN find /home/user/deploy/backups -mindepth 1 -delete 2>/dev/null || true

# Give broad write permissions so the unprivileged runtime user
# (same UID inside and outside the container) can add new files.
RUN chmod -R a+rwx /home/user

# Clean up apt caches to keep the image small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set permissions on /home/user
RUN chmod 755 /home/user

# Labels
LABEL Author="AI-Generated"
LABEL Description="Environment for web-app backup exercise with pytest pre-installed."