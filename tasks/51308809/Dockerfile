FROM ubuntu:22.04

# Help / metadata from %labels
LABEL Author="backup-engineer-exercise"
LABEL Description="Container image for the SSH backup verification task – provides initial state and pytest."

ENV HOME=/home/user

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
    chmod 0777 /home/user && \
    mkdir -p /home/user/backup_verification && \
    chmod 0777 /home/user/backup_verification && \
    mkdir -p /home/user/remote_host/.ssh && \
    chmod 0755 /home/user/remote_host/.ssh

RUN echo "# remote host authorized keys" > /home/user/remote_host/.ssh/authorized_keys && \
    chmod 0666 /home/user/remote_host/.ssh/authorized_keys