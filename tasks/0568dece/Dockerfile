FROM ubuntu:22.04

# Help / runscript content as comments
# This container is prepared for the IT-support ticket #9901 exercise.
# Run a shell inside the container to begin working:
#   apptainer exec <image.sif> /bin/bash

LABEL Author="IT-Support-Exercise" \
      Description="Base image prepared for ticket #9901 assignment. Contains ping, pytest, and /home/user directory."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        iputils-ping \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN if ! id -u user >/dev/null 2>&1; then \
        useradd --create-home --home-dir /home/user --shell /bin/bash user ; \
    fi && \
    chmod 0755 /home/user

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8