FROM ubuntu:22.04

# Install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        coreutils \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create directory structure and files
RUN mkdir -p /home/user && \
    mkdir -p /home/user/configs && \
    touch /home/user/configs/nginx.conf && \
    echo "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /home/user/configs/nginx.conf" \
        > /home/user/checksums.txt && \
    chmod 0644 /home/user/checksums.txt && \
    mkdir -p /home/user/logs && \
    chmod 0777 /home/user/logs

# Apply environment-time permissions
RUN chmod 755 /home/user

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

LABEL Author="Apptainer task setup"
LABEL Description="Environment prepared for Nginx checksum verification automation task."