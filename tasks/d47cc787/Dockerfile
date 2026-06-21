FROM ubuntu:22.04

# Labels
LABEL Author="YourName"
LABEL Description="Container image for \"disk space summary\" task – prepares /home layout and installs pytest."

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Post installation commands
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        ca-certificates \
        gnupg \
        curl && \
    pip3 install --no-cache-dir pytest && \
    groupadd -g 1000 user && \
    useradd -u 1000 -g 1000 -s /bin/bash -m -d /home/user user && \
    mkdir -p /home/user && \
    chown -R 1000:1000 /home/user && \
    chmod 755 /home/user && \
    mkdir -p /home/guest && \
    chmod 755 /home/guest && \
    dd if=/dev/urandom of=/home/guest/random.bin bs=1M count=5 && \
    chown -R 0:0 /home/guest && \
    rm -f /home/user/disk_space_summary.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Default command
CMD ["echo", "Container for disk-space summary task. Use it as a base image; no default action."]