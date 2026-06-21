# Converted from Apptainer definition file
FROM ubuntu:22.04

# Base packages and Python tooling
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tar \
        gzip \
        coreutils && \
    pip3 install --no-cache-dir pytest

# Lab initial filesystem layout
RUN mkdir -p /home/user/backup_source && \
    printf "test"  > /home/user/backup_source/test.txt && \
    printf "hello" > /home/user/backup_source/hello.txt && \
    : > /home/user/backup_source/empty.dat && \
    chmod 755 /home/user && \
    chmod 755 /home/user/backup_source && \
    chmod 644 /home/user/backup_source/test.txt \
              /home/user/backup_source/hello.txt \
              /home/user/backup_source/empty.dat

# Environment variables
ENV PATH="$PATH:$HOME/.local/bin"

# Help text from %runscript (as comments)
# Container for backup-operator exercise.
# Run your commands inside an interactive shell:
#     docker run -it <image> /bin/bash