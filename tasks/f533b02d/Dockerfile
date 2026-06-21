FROM ubuntu:22.04

# Update package index and install Python + pip
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends python3-pip python3-setuptools python3-wheel && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the automated checker
RUN pip3 install --no-cache-dir pytest

# Create a writable home directory for the unprivileged agent
RUN mkdir -p /home/user && chmod 0777 /home/user

LABEL Author="task-preparation-bot"
LABEL Description="Container for SSH-blocking snippet exercise (pytest pre-install only)"