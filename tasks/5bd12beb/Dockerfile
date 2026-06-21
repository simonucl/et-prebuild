FROM ubuntu:22.04

# Labels
LABEL Author="Capacity-Planning Task Image"
LABEL Description="Base container for capacity-planning exercise. Contains pytest and a clean /home/user."

# Update package lists and install Python tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-dev \
        ca-certificates \
        curl && \
    pip3 install --no-cache-dir pytest && \
    if ! id -u 1000 >/dev/null 2>&1; then \
        groupadd -g 1000 user && \
        useradd -m -u 1000 -g 1000 -s /bin/bash user; \
    fi && \
    mkdir -p /home/user && \
    chown -R 1000:1000 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH="/home/user/.local/bin:${PATH}"

# Set permissions on home directory
RUN chmod 755 /home/user