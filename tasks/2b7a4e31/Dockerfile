FROM ubuntu:22.04

# Labels
LABEL Author="example"
LABEL Description="Container for Python virtual-environment creation task"

# Post installation
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        ca-certificates \
        build-essential && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/venvs && \
    mkdir -p /home/user/research && \
    chmod 0777 /home/user/venvs /home/user/research && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Set working directory
WORKDIR /home/user

# Default command
CMD ["echo", "This container is intended for the Python virtual-environment setup task. Start an interactive shell with: docker run -it <container> /bin/bash"]