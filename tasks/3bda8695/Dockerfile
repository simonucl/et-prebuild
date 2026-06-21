FROM ubuntu:22.04

# Author=Apptainer_Task_Preparation
# Description="Container image for symlink creation exercise. Sets up initial directories and installs pytest."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data/dataset_v1 && \
    mkdir -p /home/user/data/dataset_v2 && \
    mkdir -p /home/user/data/dataset_v3 && \
    mkdir -p /home/user/output && \
    chmod -R 0777 /home/user

RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"