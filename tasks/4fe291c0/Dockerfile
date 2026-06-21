# Maintainer localization-task-prep
# Description "Base container for translation diagnostics exercise"

FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/local/bin:${PATH}"

RUN chmod 755 /home/user

CMD echo "Container for translation diagnostics exercise." && \
    echo "Use this shell to work on your tasks." && \
    /bin/bash