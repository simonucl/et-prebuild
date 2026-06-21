# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from %labels section
LABEL Author="ExampleBuilder"
LABEL Description="Base image for DevSecOps environment-hardening exercise – includes pytest and writable /home/user."

# %post section converted to RUN commands
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    echo "Updating package index and installing Python & pip..." && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip echo "Installing pytest for the validation test-suite..." && \
    pip3 install --no-cache-dir pytest

RUN echo "Creating writable home directory for the default user..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user

RUN echo "Ensuring /tmp is world-writable (sticky bit keeps it secure)..." && \
    chmod 1777 /tmp

RUN echo "Basic sanity check: confirm bash exists." && \
    bash -c "echo Bash is available."

# Permissions adjustment corresponding to %environment section
RUN chmod 755 /home/user

# Environment variables from %environment section
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# %runscript equivalent
CMD ["/bin/bash"]