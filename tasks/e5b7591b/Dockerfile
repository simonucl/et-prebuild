FROM ubuntu:22.04

# Labels
LABEL Author="platform-engineer"
LABEL Description="Base image for operator-test assignment. Provides Python, pytest, curl, and a non-root 'user' account with home directory /home/user. No solution artefacts are present."

# Post installation
RUN set -e && \
    echo "Updating apt repositories and installing system packages..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip curl ca-certificates && \
    echo "Creating non-root user 'user' ..." && \
    useradd -m -s /bin/bash user && \
    echo "Upgrading pip and installing pytest..." && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Default command
ENTRYPOINT []
CMD ["/bin/bash"]