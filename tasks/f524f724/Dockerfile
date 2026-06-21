FROM ubuntu:22.04

# Labels
LABEL Author="firewall-monitoring-template"
LABEL Description="Base image for the firewall monitoring exercise — pytest preinstalled, user environment prepared."

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Basic tools and Python environment
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# Create a regular user with UID 1000 (matches typical host UID)
RUN if ! id -u 1000 >/dev/null 2>&1; then \
        groupadd -g 1000 user && \
        useradd -m -u 1000 -g 1000 -s /bin/bash user; \
    fi

# Guarantee the home directory exists and is writable
RUN mkdir -p /home/user && \
    chown 1000:1000 /home/user && \
    chmod 755 /home/user

# Set working directory
WORKDIR /home/user

# Default command
CMD ["/bin/bash"]