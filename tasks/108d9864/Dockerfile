FROM ubuntu:22.04

# Labels
LABEL Author="dns-audit-task"
LABEL Description="Base image for DNS mini-audit exercise. Provides Python, pytest and common DNS utilities."

# Update package lists and install Python, pip and DNS / network utilities required for look-ups
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        dnsutils \
        iputils-ping \
        ca-certificates && \
    # Install pytest for the test harness
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    # Create the unprivileged exercise user and its home directory
    useradd -m -u 1000 -s /bin/bash user || true && \
    mkdir -p /home/user && \
    chmod 0755 /home/user && \
    # Clean up apt caches to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Set working directory
WORKDIR /home/user

# Default command
CMD ["/bin/bash"]