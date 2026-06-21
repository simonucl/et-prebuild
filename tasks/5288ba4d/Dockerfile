FROM ubuntu:22.04

# Help:
# This container provides a pristine environment for the “size on disk”
# benchmark assignment. It only includes Python 3, pytest, and a writable
# /home/user workspace; no benchmark artefacts are pre-created.

LABEL Author="Apptainer Task Setup"
LABEL Description="Base image with pytest installed and clean workspace for the benchmark assignment."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales && \
    locale-gen en_US.UTF-8 && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV PYTHONIOENCODING=utf-8