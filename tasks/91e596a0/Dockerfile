FROM ubuntu:22.04

# Help section was not provided; none added.

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-venv && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8