# Converted from Apptainer definition file
FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare staged packages directory
RUN mkdir -p /home/user/preloaded_packages && \
    chmod 0777 /home/user && \
    touch /home/user/preloaded_packages/sensor_utils-1.2.3.tar.gz && \
    touch /home/user/preloaded_packages/edge_comm-0.9.8.tar.gz && \
    chmod 0644 /home/user/preloaded_packages/*.tar.gz

# Environment settings
RUN chmod 755 /home/user
ENV PYTHONUNBUFFERED=1

# Run script equivalent
CMD ["sh", "-c", "echo \"IoT deployment exercise container. Happy hacking!\""]