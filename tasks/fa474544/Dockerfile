FROM ubuntu:22.04

# Author="Apptainer Task Setup"
# Description="Environment prepared for the release-engineer automation exercise."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tar \
        gzip \
        coreutils && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/workspace/build_output && \
    mkdir -p /home/user/workspace/scripts && \
    printf 'HelloAppBinaryV100' > /home/user/workspace/build_output/app_binary && \
    printf 'SharedObjectV100' > /home/user/workspace/build_output/libhelper.so && \
    printf 'Build artifacts for release 1.0.0' > /home/user/workspace/build_output/README.md && \
    chmod -R a+rwX /home/user

ENV PATH="$PATH:/usr/local/bin"