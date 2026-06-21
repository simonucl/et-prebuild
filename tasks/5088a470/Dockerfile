FROM ubuntu:22.04

# Help / metadata
# Author: "Container build system"
# Description: "Baseline container for the Network Diagnostics task. Includes Python, pytest, and required networking tools."

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        iputils-ping \
        iproute2 \
        netbase \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -s /bin/bash user && \
    chown -R user:user /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH="/home/user/.local/bin:${PATH}"

LABEL Author="Container build system"
LABEL Description="Baseline container for the Network Diagnostics task. Includes Python, pytest, and required networking tools."