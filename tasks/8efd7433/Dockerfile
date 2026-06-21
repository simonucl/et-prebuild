FROM ubuntu:22.04

# Update package lists and install Python & pip
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Ensure /home/user exists and is writable
RUN mkdir -p /home/user && chmod 0777 /home/user

# Apply environment-time permission adjustment equivalent
RUN chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:$PATH"

# Runscript equivalent
CMD echo "Container for the IoT edge collector exercise." && \
    echo "This container is intended to provide a clean starting environment." && \
    echo "No deliverable files or processes are created automatically."