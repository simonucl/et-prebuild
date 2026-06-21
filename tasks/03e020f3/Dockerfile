# Author: devsecops-starter
# Description: Base image for policy-as-code starter exercise. Contains Python, pytest, and an empty /home/user directory.
# Runscript behavior in Apptainer: echo "Container ready. Open a shell and follow the exercise instructions."

FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        curl && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 755 /home/user || true && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH=$PATH:/usr/local/bin