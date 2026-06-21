# Author: backup-task-preparation
# Description: Container with initial dataset and pytest installed for checksum verification task.
# Help: This container sets up the initial filesystem state for the “backup integrity” exercise. It installs pytest and prepares /home/user/source_data with required files.

FROM ubuntu:22.04

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip coreutils && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/source_data/scripts && \
    truncate -s 92  /home/user/source_data/customer_list.csv && \
    truncate -s 92  /home/user/source_data/inventory.json && \
    truncate -s 120 /home/user/source_data/readme.txt && \
    truncate -s 48  /home/user/source_data/scripts/cleanup.sh && \
    chmod 755 /home/user/source_data/scripts/cleanup.sh && \
    chmod -R a+rX /home/user/source_data

CMD ["/bin/bash"]