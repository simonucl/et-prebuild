FROM ubuntu:22.04

# Update package lists and install Python along with the venv module
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        ca-certificates && \
    # Install pytest for the automated checker
    pip3 install --no-cache-dir pytest && \
    # Ensure a writable home directory for the non-root agent
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    # Clean up APT cache to keep image size small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV HOME=/home/user

WORKDIR /home/user