FROM ubuntu:22.04

# Help / metadata from %labels
LABEL Author="Generated for edge-computing IoT configuration task"
LABEL Description="Base image with Python and pytest, initial state clean for /.iot task."

# Post section
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN useradd -m -u 1000 -s /bin/bash user

RUN chown -R user:user /home/user

# Environment section
RUN chmod 755 /home/user
ENV PATH="/home/user/.local/bin:${PATH}"