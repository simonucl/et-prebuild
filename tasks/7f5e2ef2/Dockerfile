FROM ubuntu:22.04

# Update package index and install required system packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Apply chmod from %environment
RUN chmod 755 /home/user

# Environment variables from %environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

CMD ["/bin/bash"]