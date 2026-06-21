FROM ubuntu:22.04

# Author ChatGPT
# Description "Base image for the backup-robot exercise. Includes Python, pytest, ssh-keygen and a writable /home/user directory."

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        openssh-client \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 0777 /home/user
RUN chmod 755 /home/user

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV HOME=/home/user

CMD ["/bin/bash"]