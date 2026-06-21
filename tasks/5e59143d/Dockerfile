# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# %post section
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        iputils-ping \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    if [ -x /usr/bin/ping ]; then \
        chmod u+s /usr/bin/ping || true; \
    elif [ -x /bin/ping ]; then \
        chmod u+s /bin/ping || true; \
    fi && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# %environment section
RUN chmod 755 /home/user
ENV LC_ALL=C
ENV LANG=C