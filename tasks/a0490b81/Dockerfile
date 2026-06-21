FROM ubuntu:22.04

# Author: Auto-generated
# Description: Environment for JSONPlaceholder health-check task

ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user