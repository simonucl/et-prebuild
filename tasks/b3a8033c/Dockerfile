# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Base packages and Python tooling
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state for the exercise
RUN mkdir -p /home/user/microservices/auth && \
    mkdir -p /home/user/microservices/billing && \
    printf 'Hello from auth service\n' > /home/user/microservices/auth/index.html && \
    printf 'Hello from billing service\n' > /home/user/microservices/billing/index.html && \
    rm -rf /home/user/diagnostics && \
    chmod a+rwx /home/user

# From %environment
RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin"