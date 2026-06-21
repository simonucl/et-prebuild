FROM ubuntu:22.04

# Maintainer ai-task-generator
# Description Minimal environment for the monitoring assignment with pytest pre-installed.

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    groupadd -g 1000 user && \
    useradd -m -d /home/user -s /bin/bash -u 1000 -g user user && \
    chown -R user:user /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV HOME=/home/user
ENV PATH=/home/user/.local/bin:$PATH