# syntax=docker/dockerfile:1
FROM ubuntu:22.04

LABEL Author="release-task-setup"

# Install Python and pytest for the verification suite
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state required by the task description
RUN set -e && \
    mkdir -p /home/user/releases/v1.2.2 && \
    mkdir -p /home/user/releases/v1.2.3 && \
    echo 'placeholder jar for v1.2.2' > /home/user/releases/v1.2.2/app.jar && \
    echo 'placeholder jar for v1.2.3' > /home/user/releases/v1.2.3/app.jar && \
    ln -sf /home/user/releases/v1.2.2 /home/user/releases/current && \
    chmod -R a+rwX /home/user/releases

# Environment setup
RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8