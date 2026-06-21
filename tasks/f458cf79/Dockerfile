FROM ubuntu:22.04

# Update apt index and install Python and pip
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip tooling and install pytest
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel && \
    python3 -m pip install --no-cache-dir pytest

# Ensure the canonical home directory expected by the tests exists
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Environment setup
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Set working directory
WORKDIR /home/user

# Default command
CMD ["/bin/bash"]