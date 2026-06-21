FROM ubuntu:22.04

# Install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        zip \
        gzip \
        tar \
        coreutils && \
    pip3 install --no-cache-dir pytest

# Create initial directory structure
RUN mkdir -p /home/user/artifacts/source && \
    mkdir -p /home/user/artifacts/releases && \
    mkdir -p /home/user/artifacts/staging

# Populate /home/user/artifacts/source/ with exact starting files
RUN bash -c 'for i in $(seq 1 50); do printf "BIN1\n"; done' \
        > /home/user/artifacts/source/binary1.bin
RUN bash -c 'for i in $(seq 1 50); do printf "BIN2\n"; done' \
        > /home/user/artifacts/source/binary2.bin
RUN printf 'These are sample binaries for compression test.\n' \
        > /home/user/artifacts/source/readme.txt

# Ensure appropriate permissions
RUN chmod -R a+rwX /home/user/artifacts && \
    chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

LABEL Author="artifact-manager-template"
LABEL Description="Environment for the artifact-manager task – initial state prepared."