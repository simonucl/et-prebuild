FROM ubuntu:22.04

# Help: Container for 'Lightweight on-call log backup' exercise.
# Open a shell with: apptainer exec <image>.sif /bin/bash

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/capacity/logs && \
    printf 'APP_LOG_SAMPLE\n' > /home/user/capacity/logs/app.log && \
    printf 'DB_LOG_SAMPLE\n'  > /home/user/capacity/logs/db.log && \
    printf 'SYS_LOG_SAMPLE\n' > /home/user/capacity/logs/sys.log && \
    chmod 777 /home/user/capacity && \
    chmod 755 /home/user/capacity/logs && \
    chmod 644 /home/user/capacity/logs/*.log && \
    chmod 755 /home/user