# Converted from Apptainer definition file
FROM ubuntu:22.04

# System setup and package installation
RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        iproute2 \
        iputils-ping && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    ln -sf /usr/bin/python3 /usr/local/bin/python && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Apply chmod from environment section
RUN chmod 755 /home/user

# Environment variables from %environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH