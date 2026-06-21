FROM ubuntu:22.04

# Help / metadata
# Author="Apptainer Task Preparer"
# Description="Environment for Node.js process snapshot assignment with pytest installed."

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        procps \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/webdev && \
    chmod 0755 /home/user/webdev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Apply chmod from %environment
RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin