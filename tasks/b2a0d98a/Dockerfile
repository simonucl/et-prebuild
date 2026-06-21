# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help: Container for FinOps network diagnostics exercise.
# Invoke your commands or open a shell with 'docker run -it <image>'.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        iproute2 \
        iputils-ping \
        hostname \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user && \
    mkdir -p /home/user && \
    chmod 0755 /home/user

RUN if [ ! -f /etc/resolv.conf ]; then echo "nameserver 8.8.8.8" > /etc/resolv.conf ; fi

ENV LC_ALL=C
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin