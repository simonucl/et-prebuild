# Author: Apptainer Task Setup
# Description: Environment for checksum verification task with pytest installed

FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/backups

RUN printf 'hello' > /home/user/backups/project_backup.tar.gz

RUN chmod 755 /home/user && \
    chmod 755 /home/user/backups && \
    chmod 644 /home/user/backups/project_backup.tar.gz

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8