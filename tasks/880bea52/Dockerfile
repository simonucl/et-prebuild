FROM ubuntu:22.04

# Ensure the /home/user directory exists with correct permissions
RUN set -e && \
    mkdir -p /home/user && \
    chmod 0755 /home/user

# Install Python, pip, and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Apply environment variable settings
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH