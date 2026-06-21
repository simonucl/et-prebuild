FROM ubuntu:22.04

# Labels
LABEL Author="pentest-task"
LABEL Description="Apptainer image for the vulnscan_env virtual-environment creation challenge."

# Install Python 3, venv support, pip and build tools (for possible wheel builds)
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        ca-certificates \
        build-essential && \
    # Install pytest so the grader can run its tests
    pip3 install --no-cache-dir pytest && \
    # Clean up to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a writable placeholder home; this will be bound to the real
# host home at runtime, but ensures the path exists if the bind is disabled.
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Minimal PATH setup
ENV PATH="/usr/local/bin:/usr/bin:/bin"