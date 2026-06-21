# Author: AI-Generated
# Purpose: Starting image for pentest workspace exercise

FROM ubuntu:22.04

# Refresh package index and install essentials
RUN apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        bash && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Create user if not present and set up home directory
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -d /home/user -s /bin/bash user; \
    fi && \
    chmod 0755 /home/user && \
    touch /home/user/.bashrc && \
    chown user:user /home/user/.bashrc

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Default run behavior (best Docker equivalent of exec "$@")
CMD ["bash"]