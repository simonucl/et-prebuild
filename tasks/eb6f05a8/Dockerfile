FROM ubuntu:22.04

# Labels
LABEL Author="Compliance-Apprentice-Container"
LABEL Description="Container for firewall documentation exercise with pytest pre-installed"

# Post installation commands
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user with UID 1000 whose home is /home/user
RUN if ! id -u user >/dev/null 2>&1; then \
        groupadd -g 1000 user || true; \
        useradd -m -u 1000 -g 1000 -s /bin/bash user || true; \
    fi && \
    mkdir -p /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/home/user:$PATH"

# Set working directory
WORKDIR /home/user

# Default command
CMD ["/bin/bash"]