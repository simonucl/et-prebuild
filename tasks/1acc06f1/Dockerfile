FROM ubuntu:22.04

# Install Python and pytest
RUN set -eux \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && pip3 install --no-cache-dir pytest

# Create a writable home directory for the student code
RUN mkdir -p /home/user && chmod 0777 /home/user

# Apply environment-time permissions adjustment
RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:${PATH}"