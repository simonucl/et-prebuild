# Converted from Apptainer definition
FROM ubuntu:22.04

# Install Python, pip, venv, upgrade pip, install pytest, create home, clean
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest==7.4.0 && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment settings
ENV PATH="/usr/local/bin:${PATH}"

# Ensure correct permissions at runtime
RUN chmod 755 /home/user

# No CMD needed; equivalent to Apptainer runscript exec "$@"