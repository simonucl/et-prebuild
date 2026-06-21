FROM ubuntu:22.04

# Author="Task preparation script"
# Description="Ubuntu 22.04 base with pytest installed and a clean workspace for the YAML & TOML configuration management task."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV HOME=/home/user