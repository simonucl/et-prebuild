# Based on localimage ./ubuntu_22.04.sif
FROM ubuntu:22.04

# Help text
# Author someone@example.com
# Description "Container for uptime log checksum task with pytest installed."

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN useradd -m -s /bin/bash user

RUN mkdir -p /home/user/status && \
    touch /home/user/status/uptime.log && \
    chown -R user:user /home/user/status && \
    chmod 0755 /home/user/status && \
    chmod 0644 /home/user/status/uptime.log && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin