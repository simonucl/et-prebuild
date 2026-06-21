# syntax=docker/dockerfile:1
# This container provides a clean Ubuntu 22.04 environment—complete with
# ping, traceroute, nslookup, Python 3, and pytest—ready for the “Loopback
# Interface Sanity Check” assignment. No diagnostic artefacts are present.

FROM ubuntu:22.04

LABEL Author="Automated build for Loopback Interface Sanity Check exercise"

ENV DEBIAN_FRONTEND=noninteractive
ENV HOME=/home/user

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        iputils-ping \
        traceroute \
        dnsutils \
    && pip3 install --no-cache-dir pytest \
    && mkdir -p /home/user \
    && chmod 755 /home/user \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*