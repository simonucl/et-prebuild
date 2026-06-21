FROM ubuntu:22.04

# Author backup-operator exercise setup
# Description Base container ensuring correct initial state and pytest availability.

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        time \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/backups && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/backups && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Apply environment-time permission fix
RUN chmod 755 /home/user

ENV PYTHONIOENCODING=UTF-8
ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Container runscript note
# Container for backup-operator exercise. Use this as a base — nothing to run directly.