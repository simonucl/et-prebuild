FROM ubuntu:22.04

# Basic tooling and setup
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure correct permissions for home
RUN chmod 755 /home/user

# Environment variables
ENV HOME=/home/user
ENV PYTHONDONTWRITEBYTECODE=1

# Labels
LABEL Author="Provisioning-Skeleton-Task"
LABEL Description="Base image for the provisioning skeleton exercise with pytest installed."