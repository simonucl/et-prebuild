FROM ubuntu:22.04

# Labels
LABEL Author="Task container: routine integrity-audit initial state"
LABEL Description="Container prepared for the integrity-audit task. Provides Python, pytest, and required system utilities while ensuring /home/user exists and is writable."

# Post installation
RUN set -e && \
    echo "Updating package index..." && \
    apt-get update -y && \
    echo "Installing Python, pip, and other required packages..." && \
    DEBIAN_FRONTEND=noninteractive \
        apt-get install -y --no-install-recommends \
            python3 \
            python3-pip \
            python3-setuptools \
            coreutils \
            tar \
            gzip && \
    echo "Upgrading pip and installing pytest..." && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    echo "Creating /home/user with open permissions..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    echo "Cleaning up APT caches..." && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Default command
CMD echo "This container is prepared for the integrity-audit exercise." && \
    echo "Start an interactive shell with: docker exec -it <container> /bin/bash"