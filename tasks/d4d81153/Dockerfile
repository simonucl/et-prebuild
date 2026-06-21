FROM ubuntu:22.04

# Labels
LABEL Author="Container Setup Automation"
LABEL Description="Starter image for the symlink management task, with pytest pre-installed."

# Install Python tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare the initial filesystem state expected by the exercise
RUN mkdir -p /home/user/releases

# Auth service 3.4.1
RUN mkdir -p /home/user/releases/auth-service-3.4.1 && \
    printf "Auth service build 3.4.1\n" \
        > /home/user/releases/auth-service-3.4.1/README.md

# Data service 2.1.0
RUN mkdir -p /home/user/releases/data-service-2.1.0 && \
    printf "Data service build 2.1.0\n" \
        > /home/user/releases/data-service-2.1.0/README.md

# Gateway service 1.8.7
RUN mkdir -p /home/user/releases/gateway-service-1.8.7 && \
    printf "Gateway service build 1.8.7\n" \
        > /home/user/releases/gateway-service-1.8.7/README.md

# Make /home/user writable for the non-root runtime user
RUN chmod 0777 /home/user

# Ensure the release assets are world-readable
RUN chmod -R a+r /home/user/releases

# Environment variables
ENV PYTHONUNBUFFERED=1