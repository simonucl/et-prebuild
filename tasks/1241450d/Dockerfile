# Converted from Apptainer definition file
FROM ubuntu:22.04

# Install Python, pip, venv, pytest, create directories, set permissions, clean apt
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/datasets && \
    chmod -R 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Apply chmod from %environment
RUN chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1

# Labels
LABEL Author="Apptainer Exercise Preparer"
LABEL Description="Base container for research_env virtual-environment exercise."