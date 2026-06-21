FROM ubuntu:22.04

# Author DevOps-Container-Builder
# Description "Container pre-configured for CI testing: minimal venv with pinned packages and verification files."

# Help:
# This container image contains a prepared environment for the "DevOps debug minimal
# Python-package setup" exercise.
#
# • Virtual environment: /home/user/devops_debug/venv
# • Installed packages: requests==2.28.1, boto3==1.34.59
# • Verification files:
#     – /home/user/devops_debug/logs/active_packages.log
#     – /home/user/devops_debug/logs/setup_complete.flag

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-venv \
        python3-pip \
        ca-certificates \
        curl && \
    rm -rf /var/lib/apt/lists/*

# Global pytest (needed by the grading framework)
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Prepare required directory structure under /home/user
RUN mkdir -p /home/user/devops_debug/logs

# Create the virtual environment and install the exact package versions
RUN python3 -m venv /home/user/devops_debug/venv && \
    /home/user/devops_debug/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /home/user/devops_debug/venv/bin/pip install --no-cache-dir \
        requests==2.28.1 \
        boto3==1.34.59

# Produce verification artefacts
RUN printf "requests==2.28.1\nboto3==1.34.59\n" \
        > /home/user/devops_debug/logs/active_packages.log

# Empty flag file (0-byte)
RUN : > /home/user/devops_debug/logs/setup_complete.flag

# Permissions: readable by any unprivileged user inside the container
RUN chmod -R a+rX /home/user/devops_debug && \
    chmod 755 /home/user