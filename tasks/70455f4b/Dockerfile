# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Security Scan Exercise"
LABEL Description="Container image pre-populated with a binary repository and pytest for automated assessment."

# Install Python, pip, pytest, and certificates
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Prepare required repository structure and files for the exercise
RUN set -e && \
    mkdir -p /home/user/repo/binaries && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/repo && \
    chmod 0777 /home/user/repo/binaries && \
    printf 'dummy jar content\n'            > /home/user/repo/binaries/lib1.jar && \
    printf 'malicious windows executable\n' > /home/user/repo/binaries/app.exe && \
    printf 'tgz archive placeholder\n'      > /home/user/repo/binaries/package.tar.gz && \
    chmod 0644 /home/user/repo/binaries/lib1.jar && \
    chmod 0666 /home/user/repo/binaries/app.exe && \
    chmod 0644 /home/user/repo/binaries/package.tar.gz

# Runtime environment setup
RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH