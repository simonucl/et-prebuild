# Based on localimage ./ubuntu_22.04.sif → using closest equivalent
FROM ubuntu:22.04

# Update package list and install Python + pip
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Prepare home directory
RUN mkdir -p /home/user && chmod 0777 /home/user