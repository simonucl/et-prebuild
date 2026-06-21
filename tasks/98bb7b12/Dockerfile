FROM ubuntu:22.04

# Author: db-reliability-setup
# Description: Base container for PostgreSQL backup settings exercise

LABEL Author="db-reliability-setup"
LABEL Description="Base container for PostgreSQL backup settings exercise"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user

RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"