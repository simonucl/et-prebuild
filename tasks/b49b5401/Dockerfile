FROM ubuntu:22.04

# Labels
LABEL Author="Task Preparer"
LABEL Description="Environment for NumPy version pinning task (NumPy 1.24.2 pre-installed with pytest)"

# Post installation
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir numpy==1.24.2 pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH=/usr/local/bin:$PATH

# Set working directory
WORKDIR /home/user