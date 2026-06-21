FROM ubuntu:22.04

# Labels
LABEL Author="Task prepper"
LABEL Description="Base image prepared for DNS/hostname-resolution experiment with pytest pre-installed."

# Post installation
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH="$PATH:/home/user/.local/bin"

# Set working directory
WORKDIR /home/user

# Default command
CMD ["/bin/bash", "-c", "echo 'This container is prepared for the DNS/hostname-resolution experiment.' && echo 'Invoke an interactive shell to begin working, e.g.:' && echo '    docker exec -it <container> /bin/bash'"]