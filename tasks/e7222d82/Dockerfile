FROM ubuntu:22.04

# Labels
LABEL Author="ai-generated"

# Update package lists and install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        locales && \
    locale-gen en_GB.UTF-8 && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/usr/local/bin:$PATH

# Set working directory
WORKDIR /home/user

# Default command
CMD ["/bin/bash"]