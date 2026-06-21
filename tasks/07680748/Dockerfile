# Maintainer: container-builder
# Description: Base image for localhost-resolution configuration-management exercise.

FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 0777 /home/user

ENV PATH=/usr/local/bin:$PATH

RUN chmod 755 /home/user