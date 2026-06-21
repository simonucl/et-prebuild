# syntax=docker/dockerfile:1
# Converted from Apptainer definition

FROM ubuntu:22.04

# Base tools and Python/pytest installation
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        util-linux \
        procps \
        iputils-ping \
        gawk \
        grep \
        coreutils && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment settings
ENV LC_ALL=C
ENV LANG=C
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Ensure directory permissions
RUN chmod 755 /home/user

# Default runscript behavior
CMD echo "Container is ready.  Run your benchmark script as needed."