# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer %labels
LABEL Author="Apptainer Task Prep"
LABEL Description="Environment for firewall rule task with pytest installed."

# ------------------------------------------------------------------
# %post section
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# %environment section
# ------------------------------------------------------------------
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN chmod 755 /home/user

# ------------------------------------------------------------------
# %help section
# ------------------------------------------------------------------
# This container provides a clean Ubuntu 22.04 environment with pytest
# pre-installed and write access to /home/user for completing the assignment
# that manages /home/user/firewall/mock_rules.conf.