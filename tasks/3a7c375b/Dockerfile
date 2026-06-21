FROM ubuntu:22.04

# Install Python tooling required for the autograder
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-distutils \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Set up /home/user directory structure
RUN mkdir -p /home/user && \
    chmod 0755 /home /home/user && \
    mkdir -p /home/user/shared_data && \
    chmod 0755 /home/user/shared_data && \
    touch /home/user/shared_data/suspicious.log && \
    chmod 0777 /home/user/shared_data/suspicious.log && \
    mkdir -p /home/user/shared_data/public && \
    chmod 0777 /home/user/shared_data/public

# ENV variables from %environment
ENV PYTHONIOENCODING=UTF-8
ENV PYTHONUNBUFFERED=1