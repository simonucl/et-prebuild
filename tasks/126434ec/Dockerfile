FROM ubuntu:22.04

# Labels
LABEL Author="Container Builder"
LABEL Description="Base image for self-contained name-resolution workspace exercise, with pytest installed."

# Post installation
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        procps \
        bash \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    ln -sf /usr/bin/python3 /usr/local/bin/python && \
    mkdir -p /home/user && \
    chmod 0755 /home/user && \
    rm -rf /home/user/dns_test || true && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PYTHONIOENCODING=UTF-8
ENV HOME=/home/user

# Set working directory
WORKDIR /home/user

# Default entrypoint: open an interactive shell
CMD ["/bin/bash"]