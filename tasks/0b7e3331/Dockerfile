# Author: SecurityAuditor Setup
# Description: Container for world-writable audit task
# Help: This container sets up the initial filesystem state for the
# "world-writable file audit" exercise and includes pytest for testing.

FROM ubuntu:22.04

ENV USER=user
ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/secure_data

RUN printf 'Top Secret\n'          > /home/user/secure_data/secret.conf && \
    printf 'Public data\n'         > /home/user/secure_data/public.txt && \
    printf 'Log notes\n'           > /home/user/secure_data/notes.log && \
    printf 'Project readme\n'      > /home/user/secure_data/readme.md && \
    printf 'Archive placeholder\n' > /home/user/secure_data/archive.tar.gz

RUN chmod 640 /home/user/secure_data/secret.conf && \
    chmod 666 /home/user/secure_data/public.txt && \
    chmod 606 /home/user/secure_data/notes.log && \
    chmod 644 /home/user/secure_data/readme.md && \
    chmod 600 /home/user/secure_data/archive.tar.gz && \
    chmod 755 /home/user && \
    chmod 755 /home/user/secure_data