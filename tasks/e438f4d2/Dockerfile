FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/data && \
    printf 'web01\nweb02\ndb01\ncache01\n' > /home/user/data/hosts.txt && \
    printf 'cpu=23 mem=40\ncpu=87 mem=66\ncpu=55 mem=72\ncpu=92 mem=31\n' > /home/user/data/metrics.txt && \
    chmod -R a+rwX /home/user

ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin

WORKDIR /home/user