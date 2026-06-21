FROM ubuntu:22.04

# Help / metadata from %labels
# Author: localization-task-setup
# Description: Container prepared for the localization engineer task with initial English JSON and pytest installed.

ENV HOME=/home/user

RUN set -eux \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/project

RUN printf '{"greeting":"Hello","farewell":"Goodbye"}' > /home/user/project/translations_en.json

RUN chmod -R 0777 /home/user/project \
    && chmod 0777 /home/user \
    && chmod 755 /home/user