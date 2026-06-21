# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author      "Prepared by Apptainer build script"
# Description "Ubuntu 22.04 image for backup-routine exercise with pytest and initial data set up."

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /home/user/important_data/reports && \
    mkdir -p /home/user/important_data/scripts && \
    printf 'Project Important Data\n======================\nThis directory contains confidential reports and scripts.\n' \
        > /home/user/important_data/README.md && \
    printf 'Revenue: 10000\nExpenses: 5000\nProfit: 5000\n' \
        > /home/user/important_data/reports/quarter1.txt && \
    printf 'Revenue: 12000\nExpenses: 6000\nProfit: 6000\n' \
        > /home/user/important_data/reports/quarter2.txt && \
    printf '#!/bin/bash\n# Cleanup temporary files\nrm -rf /tmp/*\n' \
        > /home/user/important_data/scripts/cleanup.sh && \
    chmod a+x /home/user/important_data/scripts/cleanup.sh && \
    chmod -R a+rX /home/user/important_data && \
    chmod 0777 /home/user

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

LABEL Author="Prepared by Apptainer build script"
LABEL Description="Ubuntu 22.04 image for backup-routine exercise with pytest and initial data set up."