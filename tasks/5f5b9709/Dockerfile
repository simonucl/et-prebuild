# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Base image for the “Nightly Build Network Diagnostic” task.
# - Contains python3 and pytest for automated grading.
# - Provides standard networking tools: hostname, uname, ip, ping, getent.
# - Leaves /home/user/build_net_diag/ absent so the learner starts from a clean slate.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        iproute2 \
        iputils-ping \
        libc-bin && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir --upgrade pip pytest

RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Ensure correct permissions at runtime equivalent
RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
ENV PYTHONUNBUFFERED="1"