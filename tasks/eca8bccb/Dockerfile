FROM ubuntu:22.04

# Update package index and install required system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        coreutils \
        findutils \
        tar \
        gzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Create a writable home directory for the normal user
RUN mkdir -p /home/user && chmod 0777 /home/user

# Apply environment-time permissions setup
RUN chmod 755 /home/user

# Environment variables
ENV PATH=/home/user/bin:$PATH