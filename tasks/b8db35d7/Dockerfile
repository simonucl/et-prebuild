# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help / labels from %labels
LABEL Author="Apptainer Automated Build"
LABEL Description="Environment for bash-package.log helper-utilities exercise – Ubuntu 22.04 with pytest pre-installed."

# %post
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# %environment
ENV PATH=/usr/local/bin:/usr/bin:/bin

RUN chmod 755 /home/user && \
    if [ ! -e /usr/bin/python ] && [ -e /usr/bin/python3 ]; then \
        ln -s /usr/bin/python3 /usr/local/bin/python || true; \
    fi