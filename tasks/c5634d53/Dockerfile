# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: ExerciseMaintainer
# Description: Container for “mobile CI pip freeze” task with pytest pre-installed.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        ca-certificates && \
    if [ ! -e /usr/bin/pip ]; then ln -s /usr/bin/pip3 /usr/bin/pip; fi && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH="$PATH:/home/user/.local/bin"

# Converted runscript
CMD echo "Container for the mobile CI pip-freeze exercise." && \
    echo "Start a shell to begin." && \
    /bin/bash