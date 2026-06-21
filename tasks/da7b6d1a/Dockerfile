FROM ubuntu:22.04

RUN set -e && \
    echo "Updating package lists and installing dependencies..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        ca-certificates && \
    echo "Installing pytest for the grading harness..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating required directory structure..." && \
    mkdir -p /home/user/releases && \
    chmod 1777 /home /home/user /home/user/releases && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8