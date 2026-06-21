# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help / metadata
# Author: SSH-Key-Pair Setup Task Container
# Purpose: Provide a clean environment with ssh-keygen and pytest installed.

ENV PATH="$PATH:/home/user/.local/bin"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        openssh-client \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -s /bin/bash user && \
    chown -R user:user /home/user && \
    chmod 755 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]