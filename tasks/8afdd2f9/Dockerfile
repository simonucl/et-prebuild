FROM ubuntu:22.04

# Help / description from labels section
# Author: QA Setup
# Description: Environment for checksum-generation exercise with pytest pre-installed.

ENV HOME=/home/user

RUN set -eux \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir pytest

RUN set -eux \
    && mkdir -p /home/user/sample_data \
    && printf 'a' > /home/user/sample_data/testfile.txt \
    && chmod 0644 /home/user/sample_data/testfile.txt \
    && chmod 0755 /home/user/sample_data \
    && chmod 0777 /home/user

LABEL Author="QA Setup" \
      Description="Environment for checksum-generation exercise with pytest pre-installed."