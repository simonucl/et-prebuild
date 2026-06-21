# syntax=docker/dockerfile:1
# Base image (converted from localimage reference)
FROM ubuntu:22.04

# Help text from %help section (none present, but labels are kept below)

# Install required packages and set up environment
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        cron \
        iputils-ping && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Commands from %environment
RUN chmod 755 /home/user
ENV LC_ALL=C
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Labels from %labels
LABEL Author="Network-Monitoring-Exercise"
LABEL Description="Base image for the network checks exercise (pytest included, clean initial state)"