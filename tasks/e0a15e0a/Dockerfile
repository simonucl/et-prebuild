FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Preparation"
LABEL Description="Base image for the SSH-key deployment exercise"

# Essential packages: SSH client for ssh-keygen, Python & pip for pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        openssh-client \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /home/user