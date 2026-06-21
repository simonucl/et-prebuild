# syntax=docker/dockerfile:1
# Author="DevSecOps Challenge Image"
# Description="Base image for SSH policy-as-code exercise with pytest pre-installed."

FROM ubuntu:22.04

ENV HOME=/home/user
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        openssh-client \
        python3 \
        python3-pip \
        ca-certificates \
        git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest pyyaml

RUN set -eux && \
    if ! id -u user >/dev/null 2>&1; then \
        useradd -m -s /bin/bash user; \
    fi && \
    mkdir -p /home/user && \
    chown -R user:user /home/user && \
    chmod 755 /home/user