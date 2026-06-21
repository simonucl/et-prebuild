FROM ubuntu:22.04

# Help / description
# Author: task-preparation
# Description: Container for low-disk-space alert rule exercise with pytest pre-installed

ENV DEBIAN_FRONTEND=noninteractive
ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/monitoring/alert_rules

RUN chmod 1777 /home/user && \
    chmod 1777 /home/user/monitoring/alert_rules