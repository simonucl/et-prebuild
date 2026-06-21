FROM ubuntu:22.04

# Labels
LABEL Author="Security-Audit-Container"
LABEL Description="Base image for SSH key-audit exercise (initial pristine state)"

# Update package index and install needed packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        openssh-client \
        ca-certificates \
        tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the testing harness
RUN pip install --no-cache-dir pytest

# Create non-privileged user "user" with home directory /home/user
RUN groupadd -g 1000 user && \
    useradd -m -d /home/user -s /bin/bash -u 1000 -g user user

# Ensure ownership of the home directory
RUN chown -R user:user /home/user

# Set permissions on home directory
RUN chmod 755 /home/user

# Basic locale settings (avoid Python warnings)
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8