FROM ubuntu:22.04

# Help / metadata from %labels
LABEL Author="ChatGPT"
LABEL Description="Container for the Archive VENV setup exercise"

# Install Python and tools
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Prepare home directory
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# %environment section
RUN chmod 755 /home/user
ENV PATH=/usr/local/bin:$PATH