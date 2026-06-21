FROM ubuntu:22.04

# Author: OpenAI ChatGPT
# Description: Base image for the OpenSSL compliance audit-trail exercise

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        openssl \
        ca-certificates && \
    apt-get clean

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    chmod 0777 /home/user

RUN chmod 755 /home/user

ENTRYPOINT ["/bin/bash", "-c", "exec \"$@\"", "--"]