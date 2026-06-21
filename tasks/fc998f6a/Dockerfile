FROM ubuntu:22.04

RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN set -eux && \
    mkdir -p /home/user/backups/full_2023_10_01/data && \
    echo "cust_data_v1"  > /home/user/backups/full_2023_10_01/data/customer.db && \
    echo "order_data_v1" > /home/user/backups/full_2023_10_01/data/orders.db && \
    echo "inv_data_v1"   > /home/user/backups/full_2023_10_01/data/inventory.db

RUN set -eux && \
    mkdir -p /home/user/project/data_link && \
    cd /home/user/project/data_link && \
    ln -s ../../backups/full_2023_10_01/data/customer.db customer.db && \
    ln -s ../../backups/full_2023_09_01/data/orders.db orders.db

RUN set -eux && \
    chmod -R a+rwX /home/user/project && \
    chmod -R a+rX /home/user/backups && \
    chmod 755 /home/user

ENV PYTHONIOENCODING=UTF-8

# Author: symlink-task-builder
# Description: Container for symlink integrity task with pytest pre-installed.
# Help:
# This image contains the initial state for the symbolic-link repair task.
# pytest is installed for automated grading.