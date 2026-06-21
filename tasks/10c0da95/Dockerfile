FROM ubuntu:22.04

# Help text
# Author: Container prepared for process-inventory snapshot task
# Description: Ubuntu 22.04 base with pytest and required utilities, ready for student execution.

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        procps \
        ca-certificates \
        curl && \
    pip3 install --no-cache-dir pytest && \
    groupadd -g 1000 user || true && \
    useradd -m -d /home/user -s /bin/bash -u 1000 -g 1000 user || true && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/home/user/.local/bin:${PATH}"

LABEL Author="Container prepared for process-inventory snapshot task"
LABEL Description="Ubuntu 22.04 base with pytest and required utilities, ready for student execution."