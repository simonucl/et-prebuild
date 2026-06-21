# Converted from Apptainer definition file
FROM ubuntu:22.04

# Update package index and install Python + pip
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install pytest
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Create the expected base home directory
RUN mkdir -p /home/user && \
    chmod 755 /home/user && \
    chown 0:0 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:${PATH}