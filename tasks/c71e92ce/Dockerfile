FROM ubuntu:22.04

# Labels
LABEL Author="task-setup"
LABEL Description="Base image for backup-restore virtual-environment exercise"

# Refresh package index and install required Python tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip && \
    # Install pytest so the grading harness can run its tests
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    # Prepare the reference home directory that the tests expect
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    # Clean up apt caches to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/user

# Default entrypoint executes whatever the user passes
ENTRYPOINT ["/bin/sh", "-c", "chmod 755 /home/user && exec \"$@\"", "--"]