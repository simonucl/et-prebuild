FROM ubuntu:22.04

# Author: Apptainer Build Script
# Description: Environment for ExampleCorp firewall-draft exercise with pytest installed.

ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-venv && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user && \
    chmod 755 /home/user

RUN mkdir -p /home/user/firewall && \
    chown -R 1000:1000 /home/user/firewall && \
    chmod 755 /home/user/firewall

LABEL Author="Apptainer Build Script" \
      Description="Environment for ExampleCorp firewall-draft exercise with pytest installed."