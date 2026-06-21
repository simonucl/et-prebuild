FROM ubuntu:22.04

# Install Python, pip, pytest and supporting utilities
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        procps && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create user and set permissions
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -d /home/user -s /bin/bash user; \
    fi && \
    mkdir -p /home/user && \
    chmod 0777 /home/user

# Guarantee a clean slate for the exercise
RUN rm -rf /home/user/sre || true

# Environment settings
ENV PATH=/usr/local/bin:/usr/bin:/bin
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Additional permission fix from %environment
RUN chmod 755 /home/user

# Run script equivalent
CMD echo "This container provides the base environment for the SRE heartbeat monitoring task."