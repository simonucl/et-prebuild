FROM ubuntu:22.04

# Help / labels
# Author: ChatGPT – Apptainer setup
# Description: Base image for the micro-service SSH key exercise with pytest pre-installed.
LABEL Author="ChatGPT – Apptainer setup"
LABEL Description="Base image for the micro-service SSH key exercise with pytest pre-installed."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        openssh-client \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    chmod 0777 /home /home/user

RUN rm -rf /home/user/.ssh/microservice_rsa \
           /home/user/.ssh/microservice_rsa.pub \
           /home/user/micro_keys \
           /home/user/ssh_setup.log || true

ENV LC_ALL=C
ENV PYTHONUNBUFFERED=1

RUN chmod 755 /home/user

CMD ["/bin/bash"]