FROM ubuntu:22.04

# From %help (none provided)

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/qa_env/bin && \
    chmod 755 /home/user /home/user/qa_env /home/user/qa_env/bin