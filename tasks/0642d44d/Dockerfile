FROM ubuntu:22.04

# Help / metadata
# Author: Apptainer Task Setup
# Description: Base image with pytest installed and a clean filesystem for the cloud migration symlink exercise.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user && \
    chown -R user:user /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH=/home/user/.local/bin:$PATH

LABEL Author="Apptainer Task Setup"
LABEL Description="Base image with pytest installed and a clean filesystem for the cloud migration symlink exercise."