FROM ubuntu:22.04

# Labels
LABEL Author="Container Preparer"
LABEL Description="Environment for local-only package bundles task with pytest pre-installed."

# Install Python, pip, and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state for the task
RUN mkdir -p /home/user/localpkgs/bash && \
    mkdir -p /home/user/localpkgs/coreutils

# Create version files with exact contents (newline-terminated)
RUN printf "5.1.16\n" > /home/user/localpkgs/bash/version.txt && \
    printf "8.32\n" > /home/user/localpkgs/coreutils/version.txt

# Ensure readable permissions for the unprivileged run-time user
RUN chmod -R 0755 /home/user

# Environment variables
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin