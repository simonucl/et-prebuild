FROM ubuntu:22.04

# Author: task-preparer
# Description: Apptainer image for process-management assignment; contains pytest and writable /home/user.
# This container sets up a minimal Ubuntu 22.04 environment with Python and pytest pre-installed,
# plus a writable /home/user directory required by the assignment.

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        procps \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PYTHONIOENCODING=UTF-8
ENV LC_ALL=C.UTF-8