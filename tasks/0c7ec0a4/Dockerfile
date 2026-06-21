FROM ubuntu:22.04

# Author: ChatGPT
# Description: Environment for the disk-write dd benchmark task
# Help:
# This container provides a minimal Ubuntu 22.04 environment with Python,
# pytest, and coreutils (for dd) pre-installed. The directory /home/user is
# writable so that learners can complete the disk-write benchmark exercise.

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        coreutils && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Equivalent of runscript default behavior
CMD ["bash"]