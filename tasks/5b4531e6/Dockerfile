FROM ubuntu:22.04

# Help:
# Base environment for the "artifact-manager" assignment.
# Provides:
#   • Python 3 + Pytest
#   • CLI tools: nc, timeout, bash
#   • Non-root user account:  user  (home: /home/user)

# Labels
LABEL Author="artifact-manager container setup"
LABEL Assignment="Repository Connectivity Diagnostics"

# Install required utilities and Python tooling
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        netcat-openbsd \
        bash \
        coreutils \
        python3 \
        python3-pip && \
    # Create a dedicated non-root user with home directory /home/user
    if ! id -u user >/dev/null 2>&1; then \
        useradd -m -s /bin/bash -u 1000 user; \
    fi && \
    # Install pytest globally (system-wide)
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    # Clean up APT caches to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:$PATH

# Default action when the container is run without arguments
CMD ["/bin/bash"]