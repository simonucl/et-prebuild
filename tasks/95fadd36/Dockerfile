FROM ubuntu:22.04

# Author: DevOpsCourse
# Purpose: Initial state for “deployment SSH key-pair” exercise

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        openssh-client && \
    pip3 install --no-cache-dir pytest && \
    adduser --disabled-password --gecos "" user && \
    mkdir -p /home/user/.ssh && \
    chmod 700 /home/user/.ssh && \
    chown -R user:user /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

CMD ["sh", "-c", "echo 'Container for the deployment SSH key-pair exercise.'"]