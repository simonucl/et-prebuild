FROM ubuntu:22.04

# Labels
LABEL Author="performance-engineer"
LABEL Description="Base image for the virtual-environment profiling task. Includes Python 3, venv support, and pytest."

# Post installation
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        python3-setuptools \
        python3-wheel \
        ca-certificates \
        curl && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH="/usr/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /home/user

# Default entrypoint
CMD ["/bin/bash"]