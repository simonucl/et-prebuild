FROM ubuntu:22.04

# Author: diagnostics-prep
# Description: Base image for the Network-Glitches Diagnostic Bundle exercise
LABEL Author="diagnostics-prep"
LABEL Description="Base image for the Network-Glitches Diagnostic Bundle exercise"

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN set -e && \
    echo "Updating APT package lists …" && \
    apt-get update -y && \
    echo "Installing required runtime tools and Python/pytest …" && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        iputils-ping \
        traceroute \
        dnsutils \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating writable /home/user directory …" && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    echo "Cleaning up APT caches …" && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

# Default runtime behavior
CMD ["/bin/bash"]