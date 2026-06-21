FROM ubuntu:22.04

# %post
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-wheel && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# %labels
LABEL Author="ChatGPT"
LABEL Description="Base image for MLOps benchmark exercise (pytest pre-installed)"
LABEL Version="1.0"