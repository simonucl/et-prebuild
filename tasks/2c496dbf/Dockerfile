FROM ubuntu:22.04

# Help / metadata from %labels and %runscript
# Author: "Container Build Script for Artifact Repository Task"
# This container sets up the initial state for the artifact repository task.
# Use 'docker run -it <image> /bin/bash' to start working on the exercise.

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/artifacts && \
    chmod 755 /home/user && \
    chmod 755 /home/user/artifacts

RUN printf 'WIDGET\n' > /home/user/artifacts/widget-1.0.0.bin && \
    printf 'GADGET\n' > /home/user/artifacts/gadget-2.1.3.bin && \
    chmod 444 /home/user/artifacts/widget-1.0.0.bin && \
    chmod 444 /home/user/artifacts/gadget-2.1.3.bin