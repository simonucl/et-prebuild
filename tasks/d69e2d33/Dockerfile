FROM ubuntu:22.04

# Author DBReliabilityEngineer
# Description Base image for network-diagnostic task – provides Python, pytest, and ping.

RUN set -eux && \
    # Update package index
    apt-get update && \
    # Install required utilities
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        iputils-ping \
        ca-certificates \
        build-essential && \
    # Install pytest for the automated test-suite
    pip3 install --no-cache-dir pytest && \
    # Create a writable home directory for the learner
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    # Clean up APT caches to reduce image size
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure pip-installed binaries are on PATH
ENV PATH=$PATH:/usr/local/bin
ENV HOME=/home/user

WORKDIR /home/user

# Runscript equivalent as default command
CMD ["echo", "Container for loopback diagnostic task. Open a shell with: docker exec -it <container> /bin/bash"]