FROM ubuntu:22.04

# Install Python, venv support, pip, and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create writable workspace directories
RUN mkdir -p /home/user/services/auth-service && \
    mkdir -p /home/user/services/setup_logs && \
    chmod -R 0777 /home/user

# Apply environment-time permissions
RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/sbin:/bin"

# Default execution behavior
CMD ["/bin/bash"]