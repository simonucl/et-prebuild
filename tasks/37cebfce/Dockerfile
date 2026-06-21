# Based on localimage source; using closest equivalent base image
FROM ubuntu:22.04

# %post
RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user/artifactory && \
    chmod 0755 /home/user && \
    chmod 0777 /home/user/artifactory && \
    (getent passwd 1000 && chown 1000:1000 /home/user/artifactory) || true && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# %environment
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONIOENCODING=UTF-8

RUN chmod 755 /home/user