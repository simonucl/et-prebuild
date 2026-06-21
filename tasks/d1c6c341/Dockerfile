FROM ubuntu:22.04

# Labels
LABEL Author="Automation-Workflow Setup"
LABEL Description="Base image prepared for workflow-automation task (Python3, venv support, pytest pre-installed)"

# Help information:
# This container provides:
#   • Python 3 with the stdlib "venv" module
#   • pytest (installed system-wide)
#   • A writable /home/user directory (permissions 0777)
# Students can create virtual environments and other artefacts under /home/user without requiring root privileges.

# Update APT package index and install prerequisites
RUN set -e && \
    echo "Updating APT package index and installing prerequisites..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        --no-install-recommends && \
    echo "Cleaning up APT caches..." && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for runtime use
RUN echo "Installing pytest for runtime use..." && \
    pip3 install --no-cache-dir pytest

# Ensure /home/user exists and is writable
RUN echo "Ensuring /home/user exists and is writable..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user

# Set environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Set working directory
WORKDIR /home/user