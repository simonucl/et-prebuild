# Minimal Ubuntu 22.04 image with Python, pip and pytest installed.
# Prepared for DevSecOps policy-as-code training exercise.

FROM ubuntu:22.04

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        git \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 0755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin

CMD ["bash"]