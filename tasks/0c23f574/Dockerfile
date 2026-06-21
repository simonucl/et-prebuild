FROM ubuntu:22.04

# Author: Permission-Hardening Task Maintainer
# Description: Base image for the “basic permission hardening” exercise.

RUN set -eux && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:${PATH}"
ENV PYTHONUNBUFFERED=1