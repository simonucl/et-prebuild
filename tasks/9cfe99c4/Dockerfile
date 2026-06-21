# Author: incident-response-task-preparer
# Description: Container with initial data and tools for the incident-response synchronisation task.
# Help:
# This container image provides the exact initial file system state
# required for the “incident-response” synchronisation exercise.

FROM ubuntu:22.04

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        rsync \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    mkdir -p /home/user/incident_data_source/images && \
    mkdir -p /home/user/incident_data_source/logs

RUN printf 'a'   > /home/user/incident_data_source/images/incident_pic1.jpg && \
    printf 'abc' > /home/user/incident_data_source/images/incident_pic2.png && \
    printf 'hello' > /home/user/incident_data_source/logs/app.log && \
    printf 'test'  > /home/user/incident_data_source/logs/error.log

RUN chmod 755 /home/user && \
    chmod 755 /home/user/incident_data_source && \
    chmod 755 /home/user/incident_data_source/images && \
    chmod 755 /home/user/incident_data_source/logs && \
    chmod 644 /home/user/incident_data_source/images/incident_pic1.jpg && \
    chmod 644 /home/user/incident_data_source/images/incident_pic2.png && \
    chmod 644 /home/user/incident_data_source/logs/app.log && \
    chmod 644 /home/user/incident_data_source/logs/error.log