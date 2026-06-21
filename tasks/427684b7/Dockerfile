# Converted from Apptainer definition file
FROM ubuntu:22.04

# Update package index and install Python and supporting tools
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Ensure writable home directory
RUN mkdir -p /home/user && chmod 777 /home/user

# Convenience symlink so `python` invokes Python 3
RUN ln -sf /usr/bin/python3 /usr/local/bin/python

# Environment variables from %environment
ENV LC_ALL=C
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Apply chmod from %environment section
RUN chmod 755 /home/user