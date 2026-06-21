# Converted from Apptainer definition
FROM ubuntu:22.04

# Update package index and install Python + pip
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Apply environment-time permissions
RUN chmod 755 /home/user

# Environment variables
ENV PATH="/home/user/.local/bin:$PATH"

# Default command
CMD ["/bin/bash"]