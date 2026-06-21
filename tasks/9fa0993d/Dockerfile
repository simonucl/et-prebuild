FROM ubuntu:22.04

LABEL Author="automated-generator"
LABEL Description="Base image for the network-health check task. Provides Python, pytest, and standard networking tools."

RUN set -e && \
    echo "Updating package index..." && \
    apt-get update -y

RUN echo "Installing required system packages..." && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        iputils-ping \
        iproute2 \
        ca-certificates

RUN echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

RUN echo "Creating non-root user 'user' with home directory /home/user ..." && \
    groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user && \
    chmod 755 /home/user

RUN echo "Cleaning up APT caches..." && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin

CMD /bin/bash -c "echo 'Container for the network-health check task.' && echo 'Invoke your commands or tests as needed.'"