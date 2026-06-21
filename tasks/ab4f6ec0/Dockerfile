# syntax=docker/dockerfile:1
# Author: "Your Name"
# Description: "Container for the 'Temporarily switch shell to UTC & C.UTF-8 and generate verification log' task. Includes pytest for automated grading."

FROM ubuntu:22.04

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    locale-gen C.UTF-8 && \
    mkdir -p /home/user && \
    chmod 0775 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN chmod 755 /home/user