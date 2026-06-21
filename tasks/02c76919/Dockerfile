# Converted from Apptainer definition file
FROM ubuntu:22.04

# Install Python, pip, pytest, and prepare /home/user
RUN set -eux \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --no-cache-dir pytest \
    && mkdir -p /home/user \
    && chmod 0777 /home/user

# Environment setup
RUN chmod 755 /home/user
ENV PATH="/home/user/.local/bin:${PATH}"