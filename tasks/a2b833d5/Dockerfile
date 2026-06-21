FROM ubuntu:22.04

# Labels
LABEL Author="network_logs_setup"
LABEL Description="Base container for network_logs assignment – ping available, pytest installed, correct initial filesystem state."

# Post installation
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        iputils-ping \
        python3-pip \
        ca-certificates \
        tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading framework
RUN pip3 install --no-cache-dir pytest

# Create the /home/user directory (but NOT /home/user/network_logs)
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Environment variables
ENV PATH="/usr/local/bin:${PATH}"

# Default command
CMD ["echo", "Container for the network_logs assignment. Use docker exec/run to start your work."]