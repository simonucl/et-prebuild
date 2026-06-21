FROM ubuntu:22.04

# Install required development tools and Python packages
RUN set -e && \
    echo "Updating package index..." && \
    apt-get update && \
    echo "Installing required development tools and Python packages..." && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        git \
        gcc \
        build-essential \
        python3 \
        python3-pip \
        coreutils \
        ca-certificates \
        curl && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating non-privileged user 'user' with home directory /home/user..." && \
    useradd -m -s /bin/bash user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /home/user