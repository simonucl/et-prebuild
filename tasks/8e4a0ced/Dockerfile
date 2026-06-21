FROM ubuntu:22.04

# Author: edge-computing-setup
# Description: Base image for IoT firmware-update exercise. Provides Python 3 and pytest, but intentionally leaves the exercise workspace empty.
# Runscript (Apptainer equivalent):
# This container prepares the environment for the IoT firmware-update exercise.
# Open a shell with: apptainer exec <image>.sif /bin/bash

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0755 /home/user && \
    chown -R 1000:1000 /home/user || true && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"