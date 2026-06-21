FROM ubuntu:22.04

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        openssh-client \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -s /bin/bash user && \
    chmod 755 /home/user && \
    rm -rf /var/lib/apt/lists/*

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8