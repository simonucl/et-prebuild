# Author finops_validator
# Description Container prepared for FinOps network diagnostics task

FROM ubuntu:22.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        iputils-ping \
        traceroute \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 755 /home/user

ENV LANG=C
ENV LC_ALL=C
ENV PATH="/home/user/.local/bin:$PATH"