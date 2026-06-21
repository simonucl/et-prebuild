FROM ubuntu:22.04

# Author="auto-generated"
# Description="Environment for checksum-creation task"

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        coreutils && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/builds/releases && \
    chmod 0777 /home/user /home/user/builds /home/user/builds/releases

RUN printf 'hello' > /home/user/builds/releases/hello-1.0.0.bin && \
    chmod 0644 /home/user/builds/releases/hello-1.0.0.bin

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"