# Author auditbot-prep
# Description "Base image for 2023-Q4 Network Diagnostics exercise. Installs tooling and pytest; intentionally leaves audit directory absent."
# Container runscript:
# echo "Container for the 2023-Q4 Network Diagnostics exercise."
# echo "Invoke an interactive shell to begin:  apptainer exec <image.sif> /bin/bash"

FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        iputils-ping \
        traceroute \
        iproute2 \
        ca-certificates \
        curl \
        gnupg \
        coreutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 0755 /home/user

ENV PYTHONUNBUFFERED=1