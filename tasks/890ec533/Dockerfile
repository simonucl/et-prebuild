FROM ubuntu:22.04

# Author: Apptainer Task Setup
# Description: Initial state for server_tokens patching challenge

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && \
    chmod 0755 /home/user

RUN printf 'server_tokens on;\n' > /home/user/nginx.conf && \
    chmod 0644 /home/user/nginx.conf

RUN rm -f /home/user/security_patch.log

ENV PATH="$PATH:/usr/local/bin"

LABEL Author="Apptainer Task Setup"
LABEL Description="Initial state for server_tokens patching challenge"