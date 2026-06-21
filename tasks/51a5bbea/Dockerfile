FROM ubuntu:22.04

LABEL Author="Checkpoint"

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales \
        tzdata && \
    rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8

RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN python3 -m pip install --no-cache-dir pytest

RUN mkdir -p /home/user/data/backups && \
    touch /home/user/data/backups/backup-20240115T231500Z.sql && \
    touch /home/user/data/backups/backup-20240116T231500Z.sql && \
    touch /home/user/data/backups/backup-20240117T231500Z.sql && \
    : > /home/user/data/backups/backup-20240115T231500Z.sql && \
    : > /home/user/data/backups/backup-20240116T231500Z.sql && \
    : > /home/user/data/backups/backup-20240117T231500Z.sql

RUN chmod 1777 /home/user && \
    mkdir -p /home/user/backup_verification && \
    chmod 777 /home/user/backup_verification && \
    chmod 755 /home/user