FROM ubuntu:22.04

# Author "Apptainer SSH-exercise base image"

RUN set -eux && \
    # Update APT index and install required packages
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        openssh-client && \
    # Install pytest for the assessment harness
    pip3 install --no-cache-dir pytest && \
    # Prepare writable workspace for the exercises
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    # Clean up APT caches to keep the image lean
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Standard PATH
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

WORKDIR /home/user