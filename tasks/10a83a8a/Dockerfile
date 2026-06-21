FROM ubuntu:22.04

# Labels
LABEL Author="container-platform-specialist"
LABEL Description="Base image for micro-service exercise with Python and pytest pre-installed."

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Update APT index and install required system packages
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/user

# Default command
CMD ["/bin/bash"]