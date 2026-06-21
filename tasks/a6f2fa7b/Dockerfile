FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Preparation"
LABEL Description="Base image for API integration virtual-environment creation task"

# Post installation commands
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        build-essential \
        ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Set working directory
WORKDIR /home/user

# Default command
CMD ["bash", "-c", "echo 'Container for API integration task. Run your commands inside this shell.' && exec /bin/bash"]