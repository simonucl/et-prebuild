FROM ubuntu:22.04

# Author: example@example.com
# Description: Base environment for firewall-tuning script exercise with pytest installed
# This container provides a clean Ubuntu 22.04 environment with Python 3 and
# pytest pre-installed. It intentionally does NOT create the files or
# directories that students will be asked to produce during the assignment.

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    echo "Updating package index and installing Python + pip..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating a non-privileged user 'user' with home directory /home/user ..." && \
    groupadd -g 1000 user && \
    useradd -m -u 1000 -g user -s /bin/bash user && \
    chown -R user:user /home/user && \
    chmod 755 /home/user && \
    echo "Container setup complete."

LABEL Author="example@example.com"
LABEL Description="Base environment for firewall-tuning script exercise with pytest installed"