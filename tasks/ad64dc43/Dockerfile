# syntax=docker/dockerfile:1
# Converted from Apptainer definition file
FROM ubuntu:22.04

# Add help text
# Author: edge-computing exercise setup
# Description: Container image for IoT fleet preparation exercise (initial pristine state)

ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/project && \
    chmod 0777 /home/user /home/user/project && \
    rm -f /home/user/project/iot_devices.db \
          /home/user/project/firmware_report.csv \
          /home/user/project/deployment.log || true

ENV PATH="$PATH:/home/user/.local/bin"

RUN chmod 755 /home/user

CMD ["/bin/bash"]