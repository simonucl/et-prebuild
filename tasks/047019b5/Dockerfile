FROM ubuntu:22.04

# Install Python, pip, and pytest
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip && \
    python3 -m pip install --no-cache-dir pytest

# Create user and group with UID/GID 1000
RUN if ! getent group 1000 >/dev/null 2>&1; then \
        groupadd -g 1000 user; \
    fi && \
    if ! id -u 1000 >/dev/null 2>&1; then \
        useradd -m -u 1000 -g 1000 user; \
    fi

# Prepare /home/user
RUN mkdir -p /home/user && chmod 0777 /home/user

# Clean apt cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/home/user/.local/bin:$PATH
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Ensure /home/user has correct permissions at runtime
RUN chmod 755 /home/user

# Default command
CMD ["/bin/bash"]