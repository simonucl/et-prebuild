# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: edge-computing-prep
# Description: Base container for IoT edge mini-stack assignment – clean slate with pytest installed.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    chmod 777 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"

RUN chmod 755 /home/user