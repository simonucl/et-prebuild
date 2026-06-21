FROM ubuntu:22.04

RUN set -e && \
    apt-get update -y && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/datasets && \
    head -c 21 /dev/zero | tr '\0' 'a' > /home/user/datasets/sample1.csv && \
    head -c 14 /dev/zero | tr '\0' 'b' > /home/user/datasets/sample2.csv && \
    head -c 13 /dev/zero | tr '\0' 'c' > /home/user/datasets/sample3.csv && \
    head -c 22 /dev/zero | tr '\0' 'd' > /home/user/datasets/config.json && \
    head -c 20 /dev/zero | tr '\0' 'e' > /home/user/datasets/meta.json && \
    chmod 777 /home/user /home/user/datasets && \
    chmod 666 /home/user/datasets/*