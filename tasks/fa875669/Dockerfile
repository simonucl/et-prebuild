FROM ubuntu:22.04

# Update APT and install Python tooling.
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip python3-setuptools python3-wheel && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading system.
RUN pip3 install --no-cache-dir pytest

# Create an unprivileged user called "user" with home directory /home/user.
RUN groupadd -g 1000 user || true && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user || true

# Ensure the home directory exists and has correct ownership.
RUN mkdir -p /home/user && chown -R 1000:1000 /home/user && chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8