FROM ubuntu:22.04

# Update apt sources and install Python & pip
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    # Create the non-root user with home directory /home/user
    useradd -m -s /bin/bash user && \
    # Make sure the new user owns its home directory
    chown -R user:user /home/user && \
    # Install pytest system-wide
    python3 -m pip install --no-cache-dir pytest && \
    # Clean up apt caches to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PATH="/home/user/.local/bin:${PATH}"

# Set permissions on home directory
RUN chmod 755 /home/user

# Default entry: just launch a shell (can be overridden by the runner)
CMD ["/bin/bash"]