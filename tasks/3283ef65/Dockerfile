FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer build script"
LABEL Description="Baseline container for the storage-administrator task"

# Post section - install packages and setup user
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -u 1000 -s /bin/bash user && \
    mkdir -p /home/user && \
    chown -R 1000:1000 /home/user && \
    chmod 0755 /home/user && \
    chmod 1777 /tmp && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Set working directory
WORKDIR /home/user

# Default command
CMD ["bash", "-c", "echo 'Docker container for the storage-administrator task.' && exec \"$@\"", "--"]