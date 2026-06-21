FROM ubuntu:22.04

# Install Python and Pytest
RUN set -e && apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        python3-venv && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 1777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure correct permissions for /home/user
RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
ENV PYTHONUNBUFFERED=1