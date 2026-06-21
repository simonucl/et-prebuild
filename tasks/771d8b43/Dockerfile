# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# %post section
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        sqlite3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# %environment section
RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:$PATH
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8