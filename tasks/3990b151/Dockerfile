FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/charlie && \
    mkdir -p /home/user/diana && \
    mkdir -p /home/user/site_admin && \
    : > /home/user/charlie/.bashrc && \
    : > /home/user/diana/.bashrc && \
    chmod -R a+rwx /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:$PATH"

LABEL Author="TimeLocaleTask"
LABEL Description="Initial container state for the time-zone & locale configuration task"
LABEL Version="1.0"