FROM ubuntu:22.04

# Author: AI
# Description: Environment for SSH-key/log automation exercise with pytest pre-installed
# Help:
#   This container provides:
#     - Ubuntu 22.04 base
#     - Python 3 and pytest
#     - OpenSSH client tools (for ssh-keygen)
#   A dedicated non-root account “user” (uid 1000) with home directory /home/user
#   is pre-created.

ENV HOME=/home/user

RUN set -e && \
    echo "Updating package index ..." && \
    apt-get update -y && \
    echo "Installing required packages ..." && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        openssh-client \
        python3 \
        python3-pip \
        ca-certificates && \
    echo "Installing pytest via pip ..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Adding non-root user 'user' (uid 1000) ..." && \
    if ! getent group 1000 >/dev/null 2>&1; then groupadd -g 1000 user; fi && \
    if ! id -u 1000 >/dev/null 2>&1; then useradd -m -u 1000 -g 1000 -s /bin/bash user; fi && \
    mkdir -p /home/user && \
    chown 1000:1000 /home/user && \
    chmod 755 /home/user && \
    echo "Cleaning up APT caches ..." && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

LABEL Author="AI"
LABEL Description="Environment for SSH-key/log automation exercise with pytest pre-installed"

USER user
WORKDIR /home/user