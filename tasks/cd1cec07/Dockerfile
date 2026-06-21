FROM ubuntu:22.04

# Labels
LABEL Author="Task Preparer"
LABEL Description="Ubuntu 22.04 base with pytest and a pre-created 'user' account for the assignment"

# Post installation
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        adduser && \
    pip3 install --no-cache-dir pytest && \
    if ! id -u user >/dev/null 2>&1; then \
        adduser --disabled-password --gecos '' user; \
    fi && \
    mkdir -p /home/user && \
    chown -R user:user /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Set proper permissions on home directory
RUN chmod 755 /home/user

# Set working directory
WORKDIR /home/user

# Default command - start shell as user
CMD ["su", "-", "user"]