FROM ubuntu:22.04

# Update package index and install Python with pip
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the automated checker
RUN pip3 install --no-cache-dir pytest

# Create the expected regular, non-privileged user and its home directory
# (the build might already contain UID 1000; ignore errors if so)
RUN useradd -m -s /bin/bash user || true && \
    mkdir -p /home/user && \
    chown -R 1000:1000 /home/user || true && \
    chmod 755 /home/user

# Make sure user-level Python packages are found first
ENV PATH="/home/user/.local/bin:${PATH}"

LABEL Maintainer="Container prepared for rsync firewall rule task (pytest included)"