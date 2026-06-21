FROM ubuntu:22.04

# Author: observability-task-setup
# Description: Container prepared with initial filesystem state for observability disk-usage task

ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        coreutils && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/observability/logs && \
    mkdir -p /home/user/observability/metrics && \
    dd if=/dev/zero of=/home/user/observability/logs/api.log bs=1024 count=1 status=none && \
    dd if=/dev/zero of=/home/user/observability/logs/web.log bs=2048 count=1 status=none && \
    dd if=/dev/zero of=/home/user/observability/metrics/metrics.json bs=1024 count=3 status=none

RUN chmod 777 /home/user/observability && \
    chmod 755 /home/user/observability/logs && \
    chmod 755 /home/user/observability/metrics && \
    chmod 644 /home/user/observability/logs/api.log && \
    chmod 644 /home/user/observability/logs/web.log && \
    chmod 644 /home/user/observability/metrics/metrics.json