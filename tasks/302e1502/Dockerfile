FROM ubuntu:22.04

# Author="Exercise Container – Network Diagnostic Log Task"
LABEL Author="Exercise Container – Network Diagnostic Log Task"

# This container provides the minimal environment for the “network-diagnostic log” exercise.
# It includes common network tools (ping, traceroute, dig, nslookup, ip) and Python with pytest for automated evaluation.

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        iputils-ping \
        traceroute \
        dnsutils \
        iproute2 \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -s /bin/bash user; \
    fi

RUN chmod 755 /home/user

ENV HOME=/home/user