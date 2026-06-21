FROM ubuntu:22.04

LABEL Author="Apptainer build system"
LABEL Description="Environment for firewall-script exercise with pytest installed."

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -d /home/user -s /bin/bash user; \
    fi

RUN mkdir -p /home/user && chmod 755 /home/user