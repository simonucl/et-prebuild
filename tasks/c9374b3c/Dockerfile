# syntax=docker/dockerfile:1
FROM ubuntu:22.04

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    adduser --disabled-password --gecos "" user && \
    mkdir -p /home/user/artie-manager/config && \
    touch /home/user/artie-manager/config/artie.conf && \
    chmod 755 /home/user /home/user/artie-manager /home/user/artie-manager/config && \
    chmod 644 /home/user/artie-manager/config/artie.conf && \
    chown -R user:user /home/user

ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin

# Equivalent of %runscript
CMD ["/bin/bash"]