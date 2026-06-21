FROM ubuntu:22.04

# Update package index and install Python + pip
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare filesystem state
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

RUN printf "# Initial Bash configuration for incident-response exercise\n" > /home/user/.bashrc && \
    chmod 0666 /home/user/.bashrc

RUN rm -f /home/user/ir_run.log

# Clean apt caches
RUN rm -rf /var/lib/apt/lists/*