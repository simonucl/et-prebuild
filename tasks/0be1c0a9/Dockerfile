FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Preparer"
LABEL Description="Base environment with ping and pytest for networking benchmark task."

# Post installation
RUN set -e && \
    echo "Updating APT package index..." && \
    apt-get update && \
    echo "Installing required system packages..." && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        iputils-ping \
        python3 \
        python3-pip && \
    echo "Installing pytest for the grader..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating writable home directory for the student..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    echo "Cleaning up APT cache to reduce image size..." && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=$PATH:/usr/local/bin

# Set working directory
WORKDIR /home/user

# Default command
CMD ["/bin/bash", "-c", "echo 'Container for the loopback latency benchmark assignment.' && echo 'Start an interactive shell with: docker exec -it <container> bash' && /bin/bash"]