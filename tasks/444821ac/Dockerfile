FROM ubuntu:22.04

# Help section
# Prepares an environment with Python, pytest, and a pre-populated internal registry.

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    REGISTRY=/home/user/container_repo && \
    mkdir -p "${REGISTRY}" && \
    touch "${REGISTRY}/backend_2.4.sif" && \
    touch "${REGISTRY}/frontend_1.8.sif" && \
    touch "${REGISTRY}/nginx_1.21.sif" && \
    touch "${REGISTRY}/worker_2.4.sif" && \
    chmod 0644 "${REGISTRY}"/*.sif && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user