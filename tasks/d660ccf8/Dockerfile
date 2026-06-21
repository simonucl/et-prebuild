FROM ubuntu:22.04

# Update package index and install required system packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        iptables \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Ensure the expected home directory exists
RUN mkdir -p /home/user && \
    chmod 0755 /home/user

WORKDIR /home/user

ENTRYPOINT ["/bin/bash", "-c", "chmod 755 /home/user && exec \"$@\"", "--"]