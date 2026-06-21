FROM ubuntu:22.04

# Author: Env-Report-Setup
# Description: Base container for env_report task; provides /home/user/project, Python, pytest, and jq.

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user/project && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/project && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

CMD echo "Container for env_report task is ready. Drop into a shell." && /bin/bash -l