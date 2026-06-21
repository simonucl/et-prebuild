FROM ubuntu:22.04

# Labels
LABEL Author="ChatGPT"
LABEL Description="Starter container for the firewall planning exercise; includes pytest."

# Ensure non-interactive APT operations
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install Python tooling
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        build-essential && \
    # Install pytest for the upcoming evaluation suite
    pip3 install --no-cache-dir pytest && \
    # Create a baseline user environment
    # The test harness expects /home/user to exist,
    # but *not* the deeper firewall directory.
    if ! id -u user >/dev/null 2>&1; then \
        useradd -m -s /bin/bash user; \
    fi && \
    # Make sure the home directory exists and is writable by 'user'
    mkdir -p /home/user && \
    chown -R user:user /home/user && \
    # Clean up APT cache to keep the image lean
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Set proper permissions on /home/user at runtime
RUN chmod 755 /home/user

# Default command
CMD ["/bin/bash"]