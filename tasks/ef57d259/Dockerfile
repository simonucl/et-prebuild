FROM ubuntu:22.04

# Update APT index and install Python tooling
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment setup
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Labels
LABEL Author="firewall-pack-prep"
LABEL Description="Starter container for firewall rules exercise (initial, pre-solution state)"