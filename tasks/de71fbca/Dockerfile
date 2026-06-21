FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/usr/local/bin:/usr/bin:/bin"

# Update package index and install required tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        sqlite3 \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/user

CMD ["bash", "-c", "echo 'Container for SQLite build-registry exercise.' && echo 'You can now run your commands.' && exec bash"]