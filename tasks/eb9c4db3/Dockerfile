FROM ubuntu:22.04

LABEL Maintainer="pip-health exercise container"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python-is-python3 && \
    pip3 install --no-cache-dir pytest && \
    python -m pip check && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/user

ENTRYPOINT ["/bin/sh", "-c", "chmod 755 /home/user && exec \"$@\"", "--"]