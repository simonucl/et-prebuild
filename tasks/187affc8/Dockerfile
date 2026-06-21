FROM ubuntu:22.04

# Help / runscript notes from Apptainer
# Default action was: exec /bin/bash

ENV PATH="/usr/local/bin:/usr/bin:${PATH}"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        diffutils \
        --no-install-recommends && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user