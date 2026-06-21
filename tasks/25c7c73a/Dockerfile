# Converted from Apptainer definition file
FROM ubuntu:22.04

# Basic utilities and Python tooling
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test harness
RUN pip3 install --no-cache-dir pytest

# Prepare the initial file-system state required by the assignment
RUN mkdir -p /home/user/dataset && \
    mkdir -p /home/user/benchmark && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/dataset && \
    chmod 0777 /home/user/benchmark && \
    printf 'id,value\n3,apple\n1,orange\n2,banana\n' > /home/user/dataset/raw.csv && \
    chmod 0644 /home/user/dataset/raw.csv

# From %environment: chmod command must be executed, exports become ENV
RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8