# Author: AutomatedContainerPrep
# Description: Base image for QA-symlink exercise – provides Python and pytest and ensures a writable /home/user.
# Help: This container supplies a pristine Ubuntu 22.04 userland with Python 3 and pytest, plus an empty, world-writable /home/user directory required by the QA-symlink assignment’s initial-state tests.

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

CMD ["bash"]