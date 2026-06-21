FROM ubuntu:22.04

# Author security-scan-task
# Description: Environment for filesystem security-sweep exercise
# Runscript: echo "Filesystem security-scan task container. Nothing to run by default."

ENV PATH=/usr/local/bin:/usr/bin:/bin

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip ca-certificates && \
    pip install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/shared /home/user/scripts /home/user/security_scan

RUN echo "#!/bin/sh\necho 'run'" > /home/user/scripts/run.sh

RUN echo "Public data" > /home/user/shared/public.txt

RUN chmod 666 /home/user/scripts/run.sh /home/user/shared/public.txt

RUN chmod 755 /home /home/user && \
    chmod 755 /home/user/shared /home/user/scripts && \
    chmod 777 /home/user/security_scan