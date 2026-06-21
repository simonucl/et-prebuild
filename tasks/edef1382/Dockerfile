FROM ubuntu:22.04

# Basic tooling and Python
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        locales

# Generate the required German UTF-8 locale
RUN locale-gen de_DE.UTF-8

# Install pytest for the automated checker
RUN pip3 install --no-cache-dir pytest

# Prepare writable home for the unprivileged runtime user
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Labels
LABEL Author="Generated for Berlin TZ / German locale task"
LABEL Description="Template image with pytest and writable /home/user; no final solution present."