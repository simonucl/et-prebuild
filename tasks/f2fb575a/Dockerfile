FROM ubuntu:22.04

# Help text
# This container image is pre-configured for the “old .sif cleanup” task.
# Five sample Singularity images are placed in /home/user/container_repo with
# the exact sizes expected by the grading tests. Pytest is installed so that
# the initial-state test suite can be executed.

LABEL Author="Auto-generated setup for Singularity cleanup task"

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/container_repo && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/container_repo

RUN truncate -s 5242880  /home/user/container_repo/alpine_3.12.sif && \
    truncate -s 7340032  /home/user/container_repo/centos_7.sif && \
    truncate -s 11288576 /home/user/container_repo/debian_10.sif && \
    truncate -s 12582912 /home/user/container_repo/ubuntu_18.04.sif && \
    truncate -s 15728640 /home/user/container_repo/ubuntu_20.04.sif && \
    chmod 0666 /home/user/container_repo/*.sif

RUN chmod 755 /home/user

ENV PATH="/home/user/.local/bin:${PATH}"