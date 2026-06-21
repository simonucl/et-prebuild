# Author: artifact-sync-preparer
# Description: Environment providing initial state for artifact sync task
# Help: This container sets up the initial filesystem layout and installs pytest
# so that students can implement and test the artifact-synchronisation task
# described in the assignment.

FROM ubuntu:22.04

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/build_server && \
    mkdir -p /home/user/deploy_server && \
    mkdir -p /home/user/sync_logs

RUN truncate -s 1024 /home/user/build_server/app-core-1.0.jar && \
    touch -t 202301151000.00 /home/user/build_server/app-core-1.0.jar

RUN truncate -s 2048 /home/user/build_server/app-web-1.0.war && \
    touch -t 202301151000.00 /home/user/build_server/app-web-1.0.war

RUN truncate -s 25 /home/user/build_server/readme.txt && \
    touch -t 202301150959.00 /home/user/build_server/readme.txt

RUN chmod 644 /home/user/build_server/app-core-1.0.jar && \
    chmod 644 /home/user/build_server/app-web-1.0.war && \
    chmod 644 /home/user/build_server/readme.txt && \
    chmod 755 /home/user/build_server && \
    chmod 777 /home/user/deploy_server && \
    chmod 777 /home/user/sync_logs