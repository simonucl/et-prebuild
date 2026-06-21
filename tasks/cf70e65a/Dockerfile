FROM ubuntu:22.04

# Labels
LABEL Author="Your Name"
LABEL Description="Base image for the benchmarking assignment. Provides python, pytest, and /usr/bin/time."

# Post installation
RUN set -e && \
    echo "Updating package lists and installing required packages..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        time \
        ca-certificates \
        git && \
    pip3 install --no-cache-dir pytest && \
    echo "Adding user 'user'..." && \
    useradd -m -s /bin/bash user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Set permissions for user home directory
RUN chmod 755 /home/user