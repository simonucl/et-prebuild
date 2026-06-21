FROM ubuntu:22.04

# Help/labels
LABEL Author="Provisioning Task Container Setup"

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    ln -sf /usr/bin/python3 /usr/local/bin/python && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user