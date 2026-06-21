FROM ubuntu:22.04

# Author System

RUN set -e && \
    echo "Updating apt cache and installing required packages..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating neutral workspace at /home/user ..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Container for systemd-timer task. Open a shell with: apptainer exec <image> /bin/bash