FROM ubuntu:22.04

# Help:
# This container provides a clean Ubuntu 22.04 environment with pytest
# installed and an empty /home/user directory ready for the student to
# perform the daily cron task staging exercise.

LABEL Author="demo"
LABEL Description="Base image for daily cron task staging exercise. Installs pytest and prepares writable /home/user without pre-creating any task files."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment permissions adjustment
RUN chmod 755 /home/user

ENV PYTHONIOENCODING=utf-8
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8