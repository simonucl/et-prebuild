FROM ubuntu:22.04

# Ensure required packages are present
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales && \
    sed -i 's/^# *\(en_US.UTF-8 UTF-8\)/\1/' /etc/locale.gen && \
    locale-gen en_US.UTF-8 && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0755 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment settings
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Help text (from %help)
# Author="Apptainer Exercise Generator"
# Description="Base image for the tz-locale report task. Initial state is clean; pytest pre-checks will verify."

LABEL Author="Apptainer Exercise Generator"
LABEL Description="Base image for the tz-locale report task. Initial state is clean; pytest pre-checks will verify."