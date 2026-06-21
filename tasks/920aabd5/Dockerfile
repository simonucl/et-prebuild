# Converted from Apptainer definition file
FROM ubuntu:22.04

# Labels from %labels
LABEL Author="Apptainer Task Preparation Bot"
LABEL Description="Environment for kernel-release logging exercise (pytest pre-installed)"

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=/usr/local/bin:$PATH

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user