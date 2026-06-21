# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help / description from labels section
LABEL Author="Automated Build"
LABEL Description="Minimal environment for ETL scheduling exercise with pytest pre-installed"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

CMD ["/bin/bash"]